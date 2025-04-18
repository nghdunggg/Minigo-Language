from AST import *
from Visitor import *
from Utils import Utils
from StaticError import *
from functools import reduce
from typing import List, Union

from StaticError import Type as StaticErrorType
from AST import Type

class FuntionType(Type):
    def __init__(self, retType: Type = VoidType(), paramTypes: List[Type] = None):
        self.retType = retType
        self.paramTypes = paramTypes if paramTypes is not None else []

    def __str__(self):
        return "FuntionType"

    def accept(self, v, param):
        return v.visitFuntionType(self, param)

class Struct:
    def __str__(self):
        return "Struct"

class Attribute:
    def __str__(self):
        return "Attribute"

class Symbol:
    def __init__(self, name, mtype, value=None):
        self.name = name
        self.mtype = mtype
        self.value = value

    def __str__(self):
        return "Symbol(" + str(self.name) + "," + str(self.mtype) + (
            "" if self.value is None else "," + str(self.value)) + ")"

class StaticChecker(BaseVisitor, Utils):

    def __init__(self, ast):
        self.ast = ast
        self.list_type: List[Union[StructType, InterfaceType]] = []
        self.list_function: List[FuncDecl] = [
            FuncDecl("getInt", [], IntType(), Block([])),
            FuncDecl("putInt", [ParamDecl("VOTIEN", IntType())], VoidType(), Block([])),
            FuncDecl("putIntLn", [ParamDecl("VOTIEN", IntType())], VoidType(), Block([])),
            FuncDecl("getFloat", [], FloatType(), Block([])),
            FuncDecl("putFloat", [ParamDecl("f", FloatType())], VoidType(), Block([])),
            FuncDecl("putFloatLn", [ParamDecl("f", FloatType())], VoidType(), Block([])),
            FuncDecl("getBool", [], BoolType(), Block([])),
            FuncDecl("putBool", [ParamDecl("b", BoolType())], VoidType(), Block([])),
            FuncDecl("putBoolLn", [ParamDecl("b", BoolType())], VoidType(), Block([])),
            FuncDecl("getString", [], StringType(), Block([])),
            FuncDecl("putString", [ParamDecl("s", StringType())], VoidType(), Block([])),
            FuncDecl("putStringLn", [ParamDecl("s", StringType())], VoidType(), Block([])),
            FuncDecl("putLn", [], VoidType(), Block([]))
        ]
        self.function_current: FuncDecl = None
    # def visit(self, ast, param):
    #     if not hasattr(ast, 'accept'):
    #         return ast
    #     else:
    #         return ast.accept(self, param)

    
    def check(self):
        self.visit(self.ast, None)

    def visitProgram(self, ast: Program, c: None):

        # Process types first.
        self.list_type = [self.visit(decl, None) for decl in ast.decl
                        if isinstance(decl, (StructType, InterfaceType))]
        # Process function declarations
        self.list_function = self.list_function + [decl for decl in ast.decl if isinstance(decl, FuncDecl)]
        
        # Process methods in structs.
        def processMethodDecl(ast: MethodDecl, env: List[List[Symbol]]) -> None:
            # Resolve the receiver type (an Id) into its actual StructType.
            st = self.lookup(ast.recType.name, self.list_type, lambda x: x.name)
            if st is None:
                raise Undeclared(Struct(), ast.recType.name + "\n")
            # If st does not have attribute 'methods', then resolve it further.
            if not hasattr(st, "methods"):
                st = self.visit(st, None)
            # Check duplicate: method name must not appear in st.methods or in the struct fields.
            if self.lookup(ast.fun.name, st.methods, lambda x: x.name) or \
            any(field[0] == ast.fun.name for field in st.elements):
                raise Redeclared(Method(), ast.fun.name + "\n")
            # Create the symbol for "this" and collect local parameters.
            this_sym = Symbol("this", st)
            local_params = tuple(map(lambda p: self.visit(p, env[0]), ast.fun.params))
            # Build the new environment for the method body.
            new_env = [[this_sym] + list(local_params)] + env
            saved_func = self.function_current
            self.function_current = ast.fun
            self.visit(ast.fun.body, new_env)
            self.function_current = saved_func
            # Add the method to the struct's method list.
            if st.methods is None:
                st.methods = []
            st.methods = st.methods + [Symbol(ast.fun.name, ast.fun.retType, ast)]
            return None

        # Process each method declaration with a new empty scope.
        for m in [m for m in ast.decl if isinstance(m, MethodDecl)]:
            processMethodDecl(m, [[]])
        
        # Build global environment...
        global_env: List[Symbol] = [
            Symbol("getInt", FuntionType(IntType(), [])),
            Symbol("putInt", FuntionType(VoidType(), [IntType()])),
            Symbol("putIntLn", FuntionType(VoidType(), [IntType()])),
            Symbol("getFloat", FuntionType(FloatType(), [])),
            Symbol("putFloat", FuntionType(VoidType(), [FloatType()])),
            Symbol("putFloatLn", FuntionType(VoidType(), [FloatType()])),
            Symbol("getBool", FuntionType(BoolType(), [])),
            Symbol("putBool", FuntionType(VoidType(), [BoolType()])),
            Symbol("putBoolLn", FuntionType(VoidType(), [BoolType()])),
            Symbol("getString", FuntionType(StringType(), [])),
            Symbol("putString", FuntionType(VoidType(), [StringType()])),
            Symbol("putStringLn", FuntionType(VoidType(), [StringType()])),
            Symbol("putLn", FuntionType(VoidType(), []))
        ]

        for d in ast.decl:
            res = self.visit(d, [global_env])
            if isinstance(res, Symbol):
                global_env.insert(0, res)
        self.global_env = global_env
        return None


    def visitStructType(self, ast: StructType, c: List[Union[StructType, InterfaceType]]) -> StructType:
        res = self.lookup(ast.name, c, lambda x: x.name)
        if res is not None:
            raise Redeclared(Struct(), ast.name + "\n")
        def visitElements(fields, ele):
            duplicate = reduce(lambda acc, f: f if acc is None and f[0] == ele[0] else acc, fields, None)
            if duplicate is not None:
                raise Redeclared(Attribute(), ele[0] + "\n")
            new_type = self.visit(ele[1], None) if hasattr(ele[1], "accept") else ele[1]
            return fields + [(ele[0], new_type)]
        ast.elements = reduce(visitElements, ast.elements, [])
        if not hasattr(ast, "methods") or ast.methods is None:
            ast.methods = []
        return ast

    def visitPrototype(self, ast: Prototype, c: List[Prototype]) -> Prototype:
        if self.lookup(ast.name, c, lambda x: x.name) is not None:
            raise Redeclared(Prototype(), ast.name + "\n")
        ast.params = tuple(map(lambda p: self.visit(p, []), ast.params))
        if hasattr(ast.retType, "accept"):
            ast.retType = self.visit(ast.retType, None)
        return ast

    def visitInterfaceType(self, ast: InterfaceType, c: List[Union[StructType, InterfaceType]]) -> InterfaceType:
        res = self.lookup(ast.name, c, lambda x: x.name)
        if res is not None:
            raise Redeclared(StaticErrorType(), ast.name + "\n")
        # Check for duplicate prototypes in the interface.
        seen = []
        new_methods = []
        for proto in ast.methods:
            if proto.name in seen:
                raise Redeclared(Prototype(), proto.name + "\n")
            seen.append(proto.name)
            new_methods.append(self.visit(proto, []))
        ast.methods = new_methods
        return ast

    def visitFuncDecl(self, ast: FuncDecl, c: List[List[Symbol]]) -> Symbol:
        if self.lookup(ast.name, c[0], lambda x: x.name):
            raise Redeclared(Function(), ast.name + "\n")
        func_symbol = Symbol(ast.name,
                             FuntionType(ast.retType, list(map(lambda p: p.parType, ast.params))),
                             ast)
        param_symbols = tuple(map(lambda p: self.visit(p, c[0]), ast.params))
        new_env = [list(param_symbols)] + c
        saved_func = self.function_current
        self.function_current = ast
        try:
            self.visit(ast.body, new_env)
        finally:
            self.function_current = saved_func
        return func_symbol

    def visitParamDecl(self, ast: ParamDecl, c: List[Symbol]) -> Symbol:
        if self.lookup(ast.parName, c, lambda x: x.name):
            raise Redeclared(Parameter(), ast.parName + "\n")
        return Symbol(ast.parName, ast.parType, None)

    def visitMethodDecl(self, ast: MethodDecl, c: List[List[Symbol]]) -> None:
        if isinstance(ast.recType, Id):
            st = self.lookup(ast.recType.name, self.list_type, lambda x: x.name)
            if st is None:
                raise Undeclared(Struct(), ast.recType.name + "\n")
        else:
            st = ast.recType

        if self.lookup(ast.fun.name, st.methods, lambda x: x.name) or \
        any(field[0] == ast.fun.name for field in st.elements):
            raise Redeclared(Method(), ast.fun.name + "\n")
        this_sym = Symbol("this", st, None)
        local_params = list(map(lambda p: self.visit(p, c[0]), ast.fun.params))
        new_env = [[this_sym] + local_params] + c

        saved_func = self.function_current
        self.function_current = ast.fun
        self.visit(ast.fun.body, new_env)
        self.function_current = saved_func
        if st.methods is None:
            st.methods = []
        st.methods = st.methods + [Symbol(ast.fun.name, ast.fun.retType, ast)]
        return None


    def lookup(self, name, lst, getName):
        if lst is None:
            return None
        for item in lst:
            
            try:
                if getName(item) == name:
                    return item
            except AttributeError:
            
                continue
        return None

    def visitVarDecl(self, ast: VarDecl, c: List[List[Symbol]]) -> Symbol:
        if self.lookup(ast.varName, c[0], lambda x: x.name) is not None:
            raise Redeclared(Variable(), ast.varName + "\n")
        if self.lookup(ast.varName, self.list_function, lambda x: x.name) is not None:
            raise Redeclared(Variable(), ast.varName + "\n")
        
        if ast.varInit is not None:
            # Special handling if the initializer is nil.
            if isinstance(ast.varInit, NilLiteral):
                if ast.varType is not None:
                    declared_type = ast.varType
                    # If the declared type is an Id, try to resolve it in list_type.
                    resolved_type = None
                    if isinstance(declared_type, Id):
                        resolved_type = self.lookup(declared_type.name, self.list_type, lambda x: x.name)
                    else:
                        resolved_type = declared_type
                    # If the resolved type is missing or one of the built-in value types then nil is not allowed.
                    if resolved_type is None or type(resolved_type) in [IntType, FloatType, BoolType, StringType]:
                        raise TypeMismatch("VarDecl(" + ast.varName + "," + str(ast.varType) + ",Nil)"+"\n")
                    # Otherwise (for structs and interfaces) nil is acceptable.
                    var_type = declared_type
                else:
                    # No declared type with nil initializer: you might want to error out or infer; here we leave it as None.
                    var_type = None
            else:
                init_type = self.visit(ast.varInit, c)
                if ast.varType is None:
                    var_type = init_type
                else:
                    declared_type = ast.varType
                    if isinstance(declared_type, FloatType) and isinstance(init_type, IntType):
                        var_type = declared_type
                    elif type(declared_type) != type(init_type):
                        raise TypeMismatch("VarDecl(" + ast.varName + "," + str(ast.varType) + "," + str(ast.varInit) + ")"+"\n")
                    else:
                        var_type = declared_type
        else:
            var_type = ast.varType

        return Symbol(ast.varName, var_type, None)


    def visitConstDecl(self, ast: ConstDecl, c: List[List[Symbol]]) -> Symbol:
        if self.lookup(ast.conName, c[0], lambda x: x.name):
            raise Redeclared(Constant(), ast.conName + "\n")
        if not isinstance(ast.iniExpr, (IntLiteral, FloatLiteral, BooleanLiteral, StringLiteral)):
            raise TypeMismatch("Id(" + ast.iniExpr.name + ")" + "\n")
        inferred_type = self.visit(ast.iniExpr, c)
        return Symbol(ast.conName, inferred_type, None)




    def visitBlock(self, ast: Block, c: List[List[Symbol]]) -> List[Symbol]:
        new_scope: List[Symbol] = []
        for member in ast.member:
            result = self.visit(member, [new_scope] + c)
            if isinstance(result, Symbol):
                if self.lookup(result.name, new_scope, lambda x: x.name) is None:
                    new_scope.insert(0, result)
        return new_scope

    def visitForBasic(self, ast: ForBasic, c: List[List[Symbol]]) -> None:
        return self.visit(Block(ast.loop.member), c)

    def visitForStep(self, ast: ForStep, c: List[List[Symbol]]) -> None:
        return self.visit(Block([ast.init] + ast.loop.member + [ast.upda]), c)

    def visitForEach(self, ast: ForEach, c: List[List[Symbol]]) -> None:
        return self.visit(Block([VarDecl(ast.idx.name, None, None),
                                 VarDecl(ast.value.name, None, None)] + ast.loop.member), c)

    def visitId(self, ast: Id, c: List[List[Symbol]]) -> Type:
        def lookup_acc(acc, scope):
            return acc if acc is not None else self.lookup(ast.name, scope, lambda x: x.name)
        res = reduce(lookup_acc, c, None)
        if res is not None and not isinstance(res.mtype, FuntionType):
            if isinstance(res.mtype, Id):
                return self.visit(res.mtype, c)
            return res.mtype
        raise Undeclared(Identifier(), ast.name + "\n")

    def visitFuncCall(self, ast: FuncCall, c: List[List[Symbol]]) -> Type:
        
        for scope in c:
            sym = self.lookup(ast.funName, scope, lambda x: x.name)
            if sym is not None:
                if isinstance(sym.mtype, FuntionType):
                    if len(ast.args) != len(sym.mtype.paramTypes):
                        raise TypeMismatch(str(ast) + "\n")
                    for arg, param_type in zip(ast.args, sym.mtype.paramTypes):
                        arg_type = self.visit(arg, c)
                        if type(arg_type) != type(param_type):
                            if not (type(param_type) == FloatType and type(arg_type) == IntType):
                                raise TypeMismatch(str(ast) + "\n")
                    return sym.mtype.retType
        
                raise Undeclared(Function(), ast.funName + "\n")
        
        raise Undeclared(Function(), ast.funName + "\n")


    # def visitFieldAccess(self, ast: FieldAccess, c: List[List[Symbol]]) -> Type:
    #     type_receiver = self.visit(ast.receiver, c)
    #     if isinstance(type_receiver, StructType):
    #         def field_acc(acc, ft):
    #             return ft[1] if acc is None and ft[0] == ast.field else acc
    #         res = reduce(field_acc, type_receiver.elements, None)
    #     else:
    #         res = None
    #     if res is None:
    #         raise Undeclared(Field(), ast.field + "\n")
    #     return res
    def visitFieldAccess(self, ast: FieldAccess, c: List[List[Symbol]]) -> Type:
        type_receiver = self.visit(ast.receiver, c)
        if isinstance(type_receiver, StructType):
            def field_acc(acc, ft):
                return ft[1] if acc is None and ft[0] == ast.field else acc
            res = reduce(field_acc, type_receiver.elements, None)
        else:
            res = None
        if res is None:
            # Instead of raising Undeclared(Field(), ...), raise a TypeMismatch error using the receiver.
            raise TypeMismatch(ast.receiver)
        return res

    def visitMethCall(self, ast: MethCall, c: List[List[Symbol]]) -> Type:
        type_receiver = self.visit(ast.receiver, c)
        if isinstance(type_receiver, StructType):
            def meth_acc(acc, m):
                return m if acc is None and m.name == ast.metName else acc
            res = reduce(meth_acc, type_receiver.methods, None)
        elif isinstance(type_receiver, InterfaceType):
            def proto_acc(acc, proto):
                return proto if acc is None and proto.name == ast.metName else acc
            res = reduce(proto_acc, type_receiver.methods, None)
        else:
            res = None
        if res is None:
            raise Undeclared(Method(), ast.metName + "\n")
        return res.mtype.retType

    def visitIntLiteral(self, ast, param): 
        return IntType()

    def visitFloatLiteral(self, ast, param): 
        return FloatType()

    def visitBooleanLiteral(self, ast, param): 
        return BoolType()

    def visitStringLiteral(self, ast, param): 
        return StringType()

    def visitArrayLiteral(self, ast, param):
        # The type of an array literal is an ArrayType whose dimensions are those in the literal
        # and element type as provided.
        return ArrayType(ast.dimens, ast.eleType)

    def visitStructLiteral(self, ast, param):
        # Look up the struct declaration by name.
        st = self.lookup(ast.name, self.list_type, lambda x: x.name)
        if st is None:
            raise Undeclared(Struct(), ast.name + "\n")
        # Optionally, you can check that each field in the literal matches one in the struct.
        return st

    def visitNilLiteral(self, ast, param):
        # Nil has no intrinsic type; its validity is checked in context.
        return None

    def visitReturn(self, ast: Return, c: List[List[Symbol]]) -> None:
        ret_expr_type = VoidType()
        if ast.expr is not None:
            ret_expr_type = self.visit(ast.expr, c)
        expected = self.function_current.retType
        if isinstance(expected, VoidType) and ast.expr is not None:
            raise TypeMismatch(str(ast) + "\n")
        if not isinstance(expected, VoidType) and ast.expr is None:
            raise TypeMismatch(str(ast) + "\n")
        if type(expected) != type(ret_expr_type):
            if not (type(expected) == FloatType and type(ret_expr_type) == IntType):
                raise TypeMismatch(str(ast) + "\n")
        return None

    def visitIf(self, ast: If, c: List[List[Symbol]]) -> None:
        cond_type = self.visit(ast.expr, c)
        if type(cond_type) != BoolType:
            raise TypeMismatch(str(ast) + "\n")
        self.visit(ast.thenStmt, c)
        if ast.elseStmt is not None:
            self.visit(ast.elseStmt, c)
        return None
    def visitAssign(self, ast, param):
        # Check that the type of lhs and rhs are compatible.
        lhsType = self.visit(ast.lhs, param)
        rhsType = self.visit(ast.rhs, param)
        # Allow assignment if both types are exactly the same,
        # or allow an int to be assigned to a float.
        if type(lhsType) != type(rhsType):
            if not (isinstance(lhsType, FloatType) and isinstance(rhsType, IntType)):
                raise TypeMismatch(ast)
        return None

    def visitContinue(self, ast, param): 
        return None

    def visitBreak(self, ast, param): 
        return None

    def format_ast(self, ast):
        # Adjust the printed representation so booleans are lower-case.
        s = str(ast)
        s = s.replace("True", "true")
        s = s.replace("False", "false")
        return s

    def visitBinaryOp(self, ast, c):
        left_type = self.visit(ast.left, c)
        right_type = self.visit(ast.right, c)
        if ast.op == "+":
            # Check for numeric addition.
            if isinstance(left_type, IntType) and isinstance(right_type, IntType):
                return IntType()
            elif (isinstance(left_type, IntType) and isinstance(right_type, FloatType)) or \
                 (isinstance(left_type, FloatType) and isinstance(right_type, IntType)) or \
                 (isinstance(left_type, FloatType) and isinstance(right_type, FloatType)):
                return FloatType()
            else:
                raise TypeMismatch("Type Mismatch: " + self.format_ast(ast) + "\n")
        elif ast.op == "%":
            # Allow modulus only for integer operands.
            if isinstance(left_type, IntType) and isinstance(right_type, IntType):
                return IntType()
            else:
                raise TypeMismatch("Type Mismatch: " + self.format_ast(ast) + "\n")
        elif ast.op in [">", "<", ">=", "<="]:
            # Relational operators: both operands must be numeric.
            if (isinstance(left_type, IntType) or isinstance(left_type, FloatType)) and \
               (isinstance(right_type, IntType) or isinstance(right_type, FloatType)):
                return BoolType()
            else:
                raise TypeMismatch("Type Mismatch: " + self.format_ast(ast) + "\n")
        elif ast.op in ["&&", "||"]:
            # Logical operators: both operands must be boolean.
            if isinstance(left_type, BoolType) and isinstance(right_type, BoolType):
                return BoolType()
            else:
                raise TypeMismatch("Type Mismatch: " + self.format_ast(ast) + "\n")
        else:
            # For any other operator, always raise error.
            raise TypeMismatch("Type Mismatch: " + self.format_ast(ast) + "\n")

    def visitVarDecl(self, ast: VarDecl, c: List[List[Symbol]]) -> Symbol:
        if self.lookup(ast.varName, c[0], lambda x: x.name) is not None:
            raise Redeclared(Variable(), ast.varName + "\n")
        if self.lookup(ast.varName, self.list_function, lambda x: x.name) is not None:
            raise Redeclared(Variable(), ast.varName + "\n")
        
        if ast.varInit is not None:
            # Special handling if the initializer is nil.
            if isinstance(ast.varInit, NilLiteral):
                if ast.varType is not None:
                    declared_type = ast.varType
                    resolved_type = None
                    if isinstance(declared_type, Id):
                        resolved_type = self.lookup(declared_type.name, self.list_type, lambda x: x.name)
                    else:
                        resolved_type = declared_type
                    if resolved_type is None or type(resolved_type) in [IntType, FloatType, BoolType, StringType]:
                        raise TypeMismatch("VarDecl(" + ast.varName + "," + str(ast.varType) + ",Nil)"+"\n")
                    var_type = declared_type
                else:
                    var_type = None
            else:
                init_type = self.visit(ast.varInit, c)
                if ast.varType is None:
                    var_type = init_type
                else:
                    declared_type = ast.varType
                    if isinstance(declared_type, FloatType) and isinstance(init_type, IntType):
                        var_type = declared_type
                    elif type(declared_type) != type(init_type):
                        # Use the initializer's printed form via format_ast to match expected error message.
                        raise TypeMismatch("Type Mismatch: " + self.format_ast(ast.varInit) + "\n")
                    else:
                        var_type = declared_type
        else:
            var_type = ast.varType

        return Symbol(ast.varName, var_type, None)


    def visitUnaryOp(self, ast, param):
        bodyType = self.visit(ast.body, param)
        if ast.op == '-':
            # Numeric negation: body must be an int or a float.
            if isinstance(bodyType, IntType) or isinstance(bodyType, FloatType):
                return bodyType
            else:
                raise TypeMismatch(ast)
        elif ast.op == '!':
            # Logical negation: body must be boolean.
            if isinstance(bodyType, BoolType):
                return BoolType()
            else:
                raise TypeMismatch(ast)
        else:
            raise TypeMismatch(ast)

    def visitArrayCell(self, ast, param):
        # The array expression must be of ArrayType.
        arrType = self.visit(ast.arr, param)
        if not isinstance(arrType, ArrayType):
            raise TypeMismatch(ast)
        # Check each index is of type IntType.
        for index in ast.idx:
            indexType = self.visit(index, param)
            if not isinstance(indexType, IntType):
                raise TypeMismatch(ast)
        # The type of the array cell is the element type.
        return arrType.eleType

    def visitIntType(self, ast: IntType, param):
        return ast

    def visitFloatType(self, ast: FloatType, param):
        return ast

    def visitBoolType(self, ast: BoolType, param):
        return ast

    def visitStringType(self, ast: StringType, param):
        return ast

    def visitVoidType(self, ast: VoidType, param):
        return ast
