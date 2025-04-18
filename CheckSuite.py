import unittest
from TestUtils import TestChecker
from AST import *


class CheckSuite(unittest.TestCase):
    # [DONE] TODO
    def test_redeclared(self):
        input = Program([
            VarDecl("a", IntType(), None),
            VarDecl("b", IntType(), None),
            VarDecl("a", IntType(), None)
        ])
        expect = "Redeclared Variable: a\n"
        self.assertTrue(TestChecker.test(input, expect, 400))
    # [DONE] TODO
    def test_type_mismatch(self):
        input = Program([VarDecl("a", IntType(), FloatLiteral(1.2))])
        expect = "Type Mismatch: VarDecl(a,IntType,FloatLiteral(1.2))\n"
        self.assertTrue(TestChecker.test(input, expect, 401))
    #[DONE] TODO :Failures
    def test_undeclared_identifier(self):
        input = Program([VarDecl("a", IntType(), Id("b"))])
        expect = "Undeclared Identifier: b\n"
        self.assertTrue(TestChecker.test(input, expect, 402))
    # [DONE] TODO
    def test_redeclared_variable(self):
        input = Program([
            VarDecl("VoTien", None, IntLiteral(1)),
            VarDecl("VoTien", None, IntLiteral(2))
        ])
        expect = "Redeclared Variable: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 403))
    # [DONE] TODO    
    def test_redeclared_constant(self):
        input = Program([
            VarDecl("VoTien", None, IntLiteral(1)),
            ConstDecl("VoTien", None, IntLiteral(2))
        ])
        expect = "Redeclared Constant: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 404))
    # [DONE] TODO
    def test_redeclared_constant_and_variable(self):
        input = Program([
            ConstDecl("VoTien", None, IntLiteral(1)),
            VarDecl("VoTien", None, IntLiteral(2))
        ])
        expect = "Redeclared Variable: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 405))
    # [DONE] TODO 
    def test_redeclared_function(self):
        input = Program([
            ConstDecl("VoTien", None, IntLiteral(1)),
            FuncDecl("VoTien", [], VoidType(), Block([Return(None)]))
        ])
        expect = "Redeclared Function: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 406))
    # [DONE] TODO
    def test_redeclared_variable_after_function(self):
        input = Program([
            FuncDecl("VoTien", [], VoidType(), Block([Return(None)])),
            VarDecl("VoTien", None, IntLiteral(1))
        ])
        expect = "Redeclared Variable: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 407))
    # [DONE] TODO
    def test_redeclared_variable_with_function_name(self):
        input = Program([
            VarDecl("getInt", None, IntLiteral(1)),
            FuncDecl("getInt", [], IntType(), Block([Return(IntLiteral(1))]))
        ])
        expect = "Redeclared Variable: getInt\n"
        self.assertTrue(TestChecker.test(input, expect, 408))
    # [DONE] TODO
    def test_function_name_as_variable(self):
        input = Program([
            VarDecl("getInt", None, IntLiteral(1))
        ])
        expect = "Redeclared Variable: getInt\n"
        self.assertTrue(TestChecker.test(input, expect, 409))
    # TODO: Error
    def test_redeclared_struct_field(self):
        input = Program([
            StructType("Votien", [("Votien", IntType())], []),
            StructType("TIEN", [
                ("Votien", StringType()),
                ("TIEN", IntType()),
                ("TIEN", FloatType())
            ], [])
        ])
        expect = "Redeclared Field: TIEN\n"
        self.assertTrue(TestChecker.test(input, expect, 410))
    # [DONE] TODO               
    def test_redeclared_method(self):
        input = Program([
            MethodDecl("v", Id("TIEN"), FuncDecl("putIntLn", [], VoidType(), Block([Return(None)]))),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([Return(None)]))),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([Return(None)]))),
            StructType("TIEN", [("Votien", IntType())], [])
        ])
        expect = "Redeclared Method: getInt\n"
        self.assertTrue(TestChecker.test(input, expect, 411))
    # [DONE] TODO        
    def test_redeclared_interface_prototype(self):
        input = Program([
            InterfaceType("VoTien", [
                Prototype("VoTien", [], VoidType()),
                Prototype("VoTien", [IntType()], VoidType())
            ])
        ])
        expect = "Redeclared Prototype: VoTien\n"
        self.assertTrue(TestChecker.test(input, expect, 412))
    # TODO: Error
    def test_redeclared_parameter(self):
        input = Program([
            FuncDecl("Votien", [ParamDecl("a", IntType()), ParamDecl("a", IntType())], VoidType(), Block([Return(None)]))
        ])
        expect = "Redeclared Parameter: a\n"
        self.assertTrue(TestChecker.test(input, expect, 413))
     # [DONE] TODO   
    def test_redeclared_variable_in_function(self):
        input = Program([
            FuncDecl("Votien", [ParamDecl("b", IntType())], VoidType(), Block([
                VarDecl("b", None, IntLiteral(1)),
                VarDecl("a", None, IntLiteral(1)),
                ConstDecl("a", None, IntLiteral(1))
            ]))
        ])
        expect = "Redeclared Constant: a\n"
        self.assertTrue(TestChecker.test(input, expect, 414))
    # [DONE] TODO
    def test_redeclared_constant_in_loop(self):
        input = Program([
            FuncDecl("Votien", [ParamDecl("b", IntType())], VoidType(), Block([
                ForStep(
                    VarDecl("a", None, IntLiteral(1)),
                    BinaryOp("<", Id("a"), IntLiteral(1)),
                    Assign(Id("a"), BinaryOp("+", Id("a"), IntLiteral(1))),
                    Block([
                        ConstDecl("a", None, IntLiteral(2))
                    ])
                )
            ]))
        ])
        expect = "Redeclared Constant: a\n"
        self.assertTrue(TestChecker.test(input, expect, 415))
    # [DONE] TODO    
    def test_undeclared_identifier_in_chain(self):
        input = Program([
            VarDecl("a", None, IntLiteral(1)),
            VarDecl("b", None, Id("a")),
            VarDecl("c", None, Id("d"))
        ])
        expect = "Undeclared Identifier: d\n"
        self.assertTrue(TestChecker.test(input, expect, 416))
    # [DONE] TODO    
    def test_undeclared_function(self):
        input = Program([
            FuncDecl("Votien", [], IntType(), Block([Return(IntLiteral(1))])),
            FuncDecl("foo", [], VoidType(), Block([
                VarDecl("b", None, FuncCall("Votien", [])),
                FuncCall("foo_votine", []),
                Return(None)
            ]))
        ])
        expect = "Undeclared Function: foo_votine\n"
        self.assertTrue(TestChecker.test(input, expect, 417))
    # TODO: Failure
    def test_undeclared_field_access(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([
                ConstDecl("c", None, FieldAccess(Id("v"), "Votien")),
                VarDecl("d", None, FieldAccess(Id("v"), "tien"))
            ])))
        ])
        expect = "Type Mismatch: Id(v)\n"
        self.assertTrue(TestChecker.test(input, expect, 418))
    # TODO: Failure   
    def test_undeclared_method_call(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("getInt", [], VoidType(), Block([
                MethCall(Id("v"), "getInt", []),
                MethCall(Id("v"), "putInt", [])
            ])))
        ])
        expect = "Undeclared Method: putInt\n"
        self.assertTrue(TestChecker.test(input, expect, 419))
    # TODO: Failure  
    def test_redeclared_struct(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            StructType("TIEN", [("v", IntType())], [])
        ])
        expect = "Redeclared Type: TIEN\n"
        self.assertTrue(TestChecker.test(input, expect, 420))
    # TODO: Error  loi giong redeclared method
    def test_redeclared_function_in_struct(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("foo", [ParamDecl("v", IntType())], VoidType(), Block([Return(None)]))),
            FuncDecl("foo", [], VoidType(), Block([Return(None)]))
        ])
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 421))
    # TODO: Failure      
    def test_function_call_chain(self):
        input = Program([
            VarDecl("a", None, FuncCall("foo", [])),
            FuncDecl("foo", [], IntType(), Block([
                VarDecl("a", None, FuncCall("koo", [])),
                VarDecl("c", None, FuncCall("getInt", [])),
                FuncCall("putInt", [Id("c")]),
                FuncCall("putIntLn", [Id("c")]),
                Return(IntLiteral(1))
            ])),
            VarDecl("d", None, FuncCall("foo", [])),
            FuncDecl("koo", [], IntType(), Block([
                VarDecl("a", None, FuncCall("foo", [])),
                Return(IntLiteral(1))
            ]))
        ])
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 422))
    # TODO: Failure            
    def test_undeclared_method_in_struct(self):
        input = Program([
            VarDecl("v", Id("TIEN"), None),
            ConstDecl("b", None, MethCall(Id("v"), "foo", [])),
            StructType("TIEN", [("a", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("foo", [], IntType(), Block([Return(IntLiteral(1))]))),
            MethodDecl("v", Id("TIEN"), FuncDecl("koo", [], IntType(), Block([Return(IntLiteral(1))]))),
            ConstDecl("c", None, MethCall(Id("v"), "koo", [])),
            ConstDecl("d", None, MethCall(Id("v"), "zoo", []))
        ])
        expect = "Type Mismatch: MethodCall(Id(v),foo,[])\n"
        self.assertTrue(TestChecker.test(input, expect, 423))
    # TODO: Failure            
    def test_undeclared_field_in_struct(self):
        input = Program([
            VarDecl("v", Id("TIEN"), None),
            ConstDecl("b", None, FieldAccess(Id("v"), "b")),
            StructType("TIEN", [("a", IntType()), ("b", IntType()), ("c", IntType())], []),
            ConstDecl("a", None, FieldAccess(Id("v"), "a")),
            ConstDecl("e", None, FieldAccess(Id("v"), "e"))
        ])
        expect = "Type Mismatch: Id(v)\n"
        self.assertTrue(TestChecker.test(input, expect, 424))
        # TODO: Failure     
    def test_redeclared_variable_in_nested_scopes(self):
        input = Program([
            ConstDecl("a", None, IntLiteral(2)),
            FuncDecl("foo", [], VoidType(), Block([
                ConstDecl("a", None, IntLiteral(1)),
                ForStep(
                    VarDecl("a", None, IntLiteral(1)),
                    BinaryOp("<", Id("a"), IntLiteral(1)),
                    Assign(Id("b"), IntLiteral(2)),
                    Block([
                        ConstDecl("b", None, IntLiteral(1))
                    ])
                )
            ]))
        ])
        expect = "Redeclared Constant: b\n"
        self.assertTrue(TestChecker.test(input, expect, 425))
        # TODO: Error  loi giong redeclared method    
    def test_redeclared_parameter_in_method(self):
        input = Program([
            StructType("TIEN", [("Votien", IntType())], []),
            MethodDecl("v", Id("TIEN"), FuncDecl("foo", [
                ParamDecl("a", IntType()),
                ParamDecl("b", IntType()),
                ParamDecl("a", IntType())
            ], VoidType(), Block([Return(None)]))),
            FuncDecl("foo", [], VoidType(), Block([Return(None)]))
        ])
        expect = "Redeclared Parameter: a\n"
        self.assertTrue(TestChecker.test(input, expect, 426))
    #[DONE] TODO
    def test_type_mismatch_in_variable_declaration(self):
        input = Program([VarDecl("v", IntType(), FloatLiteral(1.02))])
        expect = "Type Mismatch: VarDecl(v,IntType,FloatLiteral(1.02))\n"
        self.assertTrue(TestChecker.test(input, expect, 427))
    #[DONE] TODO    
    def test_type_mismatch_in_variable_declaration_with_string(self):
        input = Program([VarDecl("v", StringType(), BooleanLiteral(True))])
        expect = "Type Mismatch: VarDecl(v,StringType,BooleanLiteral(true))\n"
        self.assertTrue(TestChecker.test(input, expect, 428))
    # TODO: Error  loi giong redeclared method  
    def test_type_mismatch_in_struct_assignment(self):
        input = Program([
            StructType("S1", [("votien", IntType())], []),
            StructType("S2", [("votien", IntType())], []),
            VarDecl("v", Id("S1"), None),
            ConstDecl("x", None, Id("v")),
            VarDecl("z", Id("S1"), Id("x")),
            VarDecl("k", Id("S2"), Id("x"))
        ])
        expect = "Type Mismatch: Id(v)\n"
        self.assertTrue(TestChecker.test(input, expect, 429))
    #[DONE] TODO        
    def test_type_mismatch_in_function_return(self):
        input = Program([
            FuncDecl("foo", [], VoidType(), Block([Return(IntLiteral(1))])),
            FuncDecl("foo1", [], IntType(), Block([Return(FloatLiteral(1.0))])),
            FuncDecl("foo2", [], FloatType(), Block([Return(IntLiteral(2))]))
        ])
        expect = "Type Mismatch: Return(IntLiteral(1))\n"
        self.assertTrue(TestChecker.test(input, expect, 430))
    
    def test_type_mismatch_in_function_return_with_void(self):
        input = Program([FuncDecl("foo",[],VoidType(),Block([Return(None)])),FuncDecl("foo1",[],IntType(),Block([Return(IntLiteral(1))])),FuncDecl("foo2",[],FloatType(),Block([Return(IntLiteral(2))]))])
        expect = "Type Mismatch: Return(IntLiteral(2))\n"
        self.assertTrue(TestChecker.test(input, expect, 436))
    
    def test_type_mismatch_in_loop_variable_declaration(self):
        input = Program([
            StructType("TIEN", [("v", IntType())], []),
            VarDecl("v", Id("TIEN"), None),
            FuncDecl("foo", [], VoidType(), Block([
                ForBasic(IntLiteral(1), Block([
                    VarDecl("a", IntType(), FloatLiteral(1.02))
                ]))
            ]))
        ])
        expect = "Type Mismatch: For(IntLiteral(1),Block([VarDecl(a,IntType,FloatLiteral(1.02))]))\n"
        self.assertTrue(TestChecker.test(input, expect, 431))
     # [DONE] TODO   
    def test_type_mismatch_in_if_statement(self):
        input = Program([
            FuncDecl("foo", [], VoidType(), Block([
                If(
                    BooleanLiteral(True),
                    Block([VarDecl("a", FloatType(), FloatLiteral(1.02))]),
                    Block([VarDecl("a", IntType(), FloatLiteral(1.02))])
                )
            ]))
        ])
        expect = "Type Mismatch: VarDecl(a,IntType,FloatLiteral(1.02))\n"
        self.assertTrue(TestChecker.test(input, expect, 432))
        
    def test_type_mismatch_in_struct_and_interface_assignment(self):
        input = Program([
            StructType("S1", [("votien", IntType())], []),
            StructType("S2", [("votien", IntType())], []),
            InterfaceType("I1", [Prototype("votien1", [], VoidType())]),
            InterfaceType("I2", [Prototype("votien1", [], VoidType())]),
            MethodDecl("s", Id("S1"), FuncDecl("votien1", [], VoidType(), Block([Return(None)]))),
            VarDecl("a", Id("S1"), None),
            VarDecl("b", Id("S2"), None),
            VarDecl("c", Id("I1"), Id("a")),
            VarDecl("d", Id("I2"), Id("b"))
        ])
        expect = "Type Mismatch: VarDecl(d,Id(I2),Id(b))\n"
        self.assertTrue(TestChecker.test(input, expect, 434))
    
    def test_type_mismatch_in_variable_initialization(self):
        input = Program([VarDecl("v", FloatType(), IntLiteral(1))])
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 435))
        
    def test_cus_436(self):
        input = """
        func foo(a int) {

      foo(1);

      var foo = 1;

      foo(2); // error

 }
        """
        expect = "Undeclared Function: foo\n"
        self.assertTrue(TestChecker.test(input, expect, 436))
    
    def test_cus_437(self):
        input = """
        func foo(a int) {
            var a = 1;
 }
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 437))
        
    def test_cus_438(self):
        input = """
        func foo(a int) {
            var i int;
            for i<10 {}
 }
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 438))
   # TODO: eRROR:  'str' object has no attribute 'accept' 
    def test_cus_439(self):
        input = """

        func foo(a int) {
            p:=Person{name:"Alice",age:30}
            q:=Person{}
 }        
 type Person struct {
            name string;
            age int;
        }
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 439))
    # TODO: eRROR:  'str' object has no attribute 'accept'
    def test_cus_440(self):
        input = """

        func foo(z int) {
            a := [2]int {2,1}
            b := [2]float {1,2}
            b := a
            var c float = 1.0
            c := 2
 }        
 type Person struct {
            name string;
            age int;
        }
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 440))
# TODO
    def test_015(self):
        input =  """ 
type TIEN struct {
    Votien int;
}

func (v TIEN) getInt () {
    const c = v.Votien;
    var d = v.tien;
}
        """
        self.assertTrue(TestChecker.test(input, "Type Mismatch: Id(v)\n", 15))

    def test_001(self):
        """
var VoTien = 1; 
var VoTien = 2;
        """
        input = Program([VarDecl("VoTien", None,IntLiteral(1)),VarDecl("VoTien", None,IntLiteral(2))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: VoTien\n", 1))

    def test_002(self):
        """
var VoTien = 1; 
const VoTien = 2;
        """
        input = Program([VarDecl("VoTien", None,IntLiteral(1)),ConstDecl("VoTien",None,IntLiteral(2))])
        self.assertTrue(TestChecker.test(input, "Redeclared Constant: VoTien\n", 1))

    def test_003(self):
        """
const VoTien = 1; 
var VoTien = 2;
        """
        input = Program([ConstDecl("VoTien",None,IntLiteral(1)),VarDecl("VoTien", None,IntLiteral(2))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: VoTien\n", 1))

    def test_004(self):
        """
const VoTien = 1; 
func VoTien () {return;}
        """
        input = Program([ConstDecl("VoTien",None,IntLiteral(1)),FuncDecl("VoTien",[],VoidType(),Block([Return(None)]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Function: VoTien\n", 1))

    def test_005(self):
        """ 
func VoTien () {return;}
var VoTien = 1;
        """
        input = Program([FuncDecl("VoTien",[],VoidType(),Block([Return(None)])),VarDecl("VoTien", None,IntLiteral(1))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: VoTien\n", 1))

    def test_006(self):
        """ 
var getInt = 1;
        """
        input = Program([VarDecl("getInt", None,IntLiteral(1))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: getInt\n", 1))

    def test_007(self):
        """ 
type  Votien struct {
    Votien int;
}
type TIEN struct {
    Votien string;
    TIEN int;
    TIEN float;
}
        """
        input = Program([StructType("Votien",[("Votien",IntType())],[]),StructType("TIEN",[("Votien",StringType()),("TIEN",IntType()),("TIEN",FloatType())],[])])
        self.assertTrue(TestChecker.test(input, "Redeclared Field: TIEN\n", 1))

    def test_008(self):
        """ 
func (v TIEN) putIntLn () {return;}
func (v TIEN) getInt () {return;}
func (v TIEN) getInt () {return;}
type TIEN struct {
    Votien int;
}
        """
        input = Program([MethodDecl("v",Id("TIEN"),FuncDecl("putIntLn",[],VoidType(),Block([Return(None)]))),MethodDecl("v",Id("TIEN"),FuncDecl("getInt",[],VoidType(),Block([Return(None)]))),MethodDecl("v",Id("TIEN"),FuncDecl("getInt",[],VoidType(),Block([Return(None)]))), StructType("TIEN",[("Votien",IntType())],[])])
        self.assertTrue(TestChecker.test(input, "Redeclared Method: getInt\n", 1))

    def test_009(self):
        """ 
type VoTien interface {
    VoTien ();
    VoTien (a int);
}
        """
        input = Program([InterfaceType("VoTien",[Prototype("VoTien",[],VoidType()),Prototype("VoTien",[IntType()],VoidType())])])
        self.assertTrue(TestChecker.test(input, "Redeclared Prototype: VoTien\n", 1))

    def test_010(self):
        """ 
func Votien (a, a int) {return;}
        """
        input = Program([FuncDecl("Votien",[ParamDecl("a",IntType()),ParamDecl("a",IntType())],VoidType(),Block([Return(None)]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Parameter: a\n", 1))

    def test_011(self):
        """ 
func Votien (b int) {
    var b = 1;
    var a = 1;
    const a = 1;
}
        """
        input = Program([FuncDecl("Votien",[ParamDecl("b",IntType())],VoidType(),Block([VarDecl("b", None,IntLiteral(1)),VarDecl("a", None,IntLiteral(1)),ConstDecl("a",None,IntLiteral(1))]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Constant: a\n", 1))

    def test_012(self):
        """ 
func Votien (b int) {
    for var a = 1; a < 1; a += 1 {
        const a = 2;
    }
}
        """
        input = Program([FuncDecl("Votien",[ParamDecl("b",IntType())],VoidType(),Block([ForStep(VarDecl("a", None,IntLiteral(1)),BinaryOp("<", Id("a"), IntLiteral(1)),Assign(Id("a"),BinaryOp("+", Id("a"), IntLiteral(1))),Block([ConstDecl("a",None,IntLiteral(2))]))]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Constant: a\n", 1))

    def test_013(self):
        """ 
var a = 1;
var b = a;
var c = d;
        """
        input = Program([VarDecl("a", None,IntLiteral(1)),VarDecl("b", None,Id("a")),VarDecl("c", None,Id("d"))])
        self.assertTrue(TestChecker.test(input, "Undeclared Identifier: d\n", 1))

    def test_014(self):
        """ 
func Votien () int {return 1;}

fun foo () {
    var b = Votien();
    foo_votine();
    return;
}
        """
        input = Program([FuncDecl("Votien",[],IntType(),Block([Return(IntLiteral(1))])),FuncDecl("foo",[],VoidType(),Block([VarDecl("b", None,FuncCall("Votien",[])),FuncCall("foo_votine",[]),Return(None)]))])
        self.assertTrue(TestChecker.test(input, "Undeclared Function: foo_votine\n", 14))

    def test_015(self):
        input = Program([StructType("TIEN",[("Votien",IntType())],[]),MethodDecl("v",Id("TIEN"),FuncDecl("getInt",[],VoidType(),Block([ConstDecl("c",None,FieldAccess(Id("v"),"Votien")),VarDecl("d", None,FieldAccess(Id("v"),"tien"))])))])

        """ 
type TIEN struct {
    Votien int;
}

func (v TIEN) getInt () {
    const c = v.Votien;
    var d = v.tien;
}
        """
        self.assertTrue(TestChecker.test(input, "Type Mismatch: Id(v)\n", 15))

    def test_016(self):
        """ 
type TIEN struct {
    Votien int;
}

func (v TIEN) getInt () {
    v.getInt ();
    v.putInt ();
}
        """
        input = Program([StructType("TIEN",[("Votien",IntType())],[]),MethodDecl("v",Id("TIEN"),FuncDecl("getInt",[],VoidType(),Block([MethCall(Id("v"),"getInt",[]),MethCall(Id("v"),"putInt",[])])))])
        self.assertTrue(TestChecker.test(input, "Undeclared Method: putInt\n", 16))
    
    def test_017(self):
        """ 
type TIEN struct {Votien int;}
type TIEN struct {v int;}
        """
        input = Program([StructType("TIEN",[("Votien",IntType())],[]),StructType("TIEN",[("v",IntType())],[])])
        self.assertTrue(TestChecker.test(input, "Redeclared Type: TIEN\n", 17))

    def test_018(self):
        """ 
type TIEN struct {
    a int;
    b int;
    a float;
}
        """
        input = Program([StructType("TIEN",[("a",IntType()),("b",IntType()),("a",FloatType())],[])])
        self.assertTrue(TestChecker.test(input, "Redeclared Field: a\n", 18))

    def test_019(self):
        """
func getString() {return;}
        """
        input = Program([FuncDecl("getString",[],VoidType(),Block([Return(None)]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Function: getString\n", 19))

    def test_032(self):
        """ 
func getString() {return;}
        """
        input = Program([FuncDecl("getString",[],VoidType(),Block([Return(None)]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Function: getString\n", 32))

    def test_033(self):
        """ 
func putStringLn() {return;}
        """
        input = Program([FuncDecl("putStringLn",[],VoidType(),Block([Return(None)]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Function: putStringLn\n", 33))

    def test_044(self):
        input = """
type TIEN struct {
    Votien int;
}
func (v TIEN) foo (v int) {return;}
func foo () {return;}
        """
        self.assertTrue(TestChecker.test(input, "", 44))

    def test_051(self):
        input = Program([ConstDecl("a",None,IntLiteral(2)),FuncDecl("foo",[],VoidType(),Block([ConstDecl("a",None,IntLiteral(1)),ForStep(VarDecl("a", None,IntLiteral(1)),BinaryOp("<", Id("a"), IntLiteral(1)),Assign(Id("b"),IntLiteral(2)),Block([ConstDecl("b",None,IntLiteral(1))]))]))])
        """
const a = 2;
func foo () {
    const a = 1;
    for var a = 1; a < 1; b := 2 {
        const b = 1;
    }
}
        """
        self.assertTrue(TestChecker.test(input, "Redeclared Constant: b\n", 51))

    def test_052(self):
        input = Program([ConstDecl("a",None,IntLiteral(2)),FuncDecl("foo",[],VoidType(),Block([ConstDecl("a",None,IntLiteral(1)),ForBasic(BinaryOp("<", Id("a"), IntLiteral(1)),Block([ConstDecl("a",None,IntLiteral(1)),ForBasic(BinaryOp("<", Id("a"), IntLiteral(1)),Block([ConstDecl("a",None,IntLiteral(1)),ConstDecl("b",None,IntLiteral(1))])),ConstDecl("b",None,IntLiteral(1)),VarDecl("a", None,IntLiteral(1))]))]))])
        """
const a = 2;
func foo () {
    const a = 1;
    for a < 1 {
        const a = 1;
        for a < 1 {
            const a = 1;
            const b = 1;
        }
        const b = 1;
        var a = 1;
    }
}
        """
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: a\n", 52))

    def test_053(self):
        input = """
func foo () {
    const a = 1;
    for a, b := range [3]int {1, 2, 3} {
        var b = 1;
    }
}
        """
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: b\n", 53))

    def test_061(self):
        input = """
var a = foo();
func foo () int {
    var a =  koo();
    var c = getInt();
    putInt(c);
    putIntLn(c);
    return 1;
}
var d = foo();
func koo () int {
    var a =  foo ();
    return 1;
}
        """
        self.assertTrue(TestChecker.test(input, "", 61))

    def test_065(self):
        """ 
var v TIEN;
const b = v.b;        
type TIEN struct {
    a int;
    b int;
    c int;
}
const a = v.a;
const e = v.e;
        """
        input = Program([VarDecl("v",Id("TIEN"), None),ConstDecl("b",None,FieldAccess(Id("v"),"b")),StructType("TIEN",[("a",IntType()),("b",IntType()),("c",IntType())],[]),ConstDecl("a",None,FieldAccess(Id("v"),"a")),ConstDecl("e",None,FieldAccess(Id("v"),"e"))])
        self.assertTrue(TestChecker.test(input, "Type Mismatch: Id(v)\n", 65))

    def test_071(self):
        input =  """  
var v TIEN;      
type TIEN struct {
    a int;
} 
type VO interface {
    foo() int;
}

func (v TIEN) foo() int {return 1;}
func (b TIEN) koo() {b.koo();}
func foo() {
    var x VO;  
    const b = x.foo(); 
    x.koo(); 
}
        """
        self.assertTrue(TestChecker.test(input, "Type Mismatch: MethodCall(Id(x),foo,[])\n", 71)) 

    def test_076(self):
        input = Program([StructType("S1",[("votien",IntType())],[]),StructType("S2",[("votien",IntType())],[]),VarDecl("v",Id("S1"), None),ConstDecl("x",None,Id("v")),VarDecl("z",Id("S1"),Id("x")),VarDecl("k",Id("S2"),Id("x"))])
        """
type S1 struct {votien int;}
type S2 struct {votien int;}

var v S1;
const x = v;
var z S1 = x;
var k S2 = x;
        """
        self.assertTrue(TestChecker.test(input, "Type Mismatch: Id(v)\n", 76))

    def test_077(self):
        input = Program([InterfaceType("I1",[Prototype("votien",[],VoidType())]),InterfaceType("I2",[Prototype("votien",[],VoidType())]),VarDecl("v",Id("I1"), None),ConstDecl("x",None,Id("v")),VarDecl("z",Id("I1"),Id("x")),VarDecl("k",Id("I2"),Id("x"))])
        expect = "Type Mismatch: Id(v)\n"
        self.assertTrue(TestChecker.test(input, expect, 77))

    def test_079(self):
        input = Program([StructType("S1",[("vo",IntType())],[]),StructType("S2",[("vo",IntType())],[]),InterfaceType("I1",[Prototype("votien",[],VoidType())]),InterfaceType("I2",[Prototype("votien",[],IntType())]),MethodDecl("s",Id("S1"),FuncDecl("votien",[],VoidType(),Block([Return(None)]))),VarDecl("a",Id("S1"), None),VarDecl("b",Id("S2"), None),VarDecl("c",Id("I2"),Id("a"))])
        """
type S1 struct {vo int;}
type S2 struct {vo int;}
type I1 interface {votien();}
type I2 interface {votien() int;}

func (s S1) votien() {return;}

var a S1;
var b S2;
var c I2 = a; 
        """
        self.assertTrue(TestChecker.test(input, "Type Mismatch: VarDecl(c,Id(I2),Id(a))\n", 79))

    def test_080(self):
        input = Program([StructType("S1",[("vo",IntType())],[]),StructType("S2",[("vo",IntType())],[]),InterfaceType("I1",[Prototype("votien",[],Id("S1"))]),InterfaceType("I2",[Prototype("votien",[],Id("S2"))]),MethodDecl("s",Id("S1"),FuncDecl("votien",[],Id("S1"),Block([Return(Id("s"))]))),VarDecl("a",Id("S1"), None),VarDecl("c",Id("I1"),Id("a")),VarDecl("d",Id("I2"),Id("a"))])
        """
type S1 struct {vo int;}
type S2 struct {vo int;}
type I1 interface {votien() S1;}
type I2 interface {votien() S2;}

func (s S1) votien() S1 {return s;}

var a S1;
var c I1 = a;
var d I2 = a;
        """
        self.assertTrue(TestChecker.test(input, "Type Mismatch: VarDecl(d,Id(I2),Id(a))\n", 80))

    def test_082(self):
        input = Program([StructType("S1",[("votien",IntType())],[]),StructType("S2",[("votien",IntType())],[]),InterfaceType("I1",[Prototype("votien1",[IntType(),IntType()],Id("S1"))]),InterfaceType("I2",[Prototype("votien1",[IntType(),FloatType()],Id("S1"))]),MethodDecl("s",Id("S1"),FuncDecl("votien1",[ParamDecl("a",IntType()),ParamDecl("b",IntType())],Id("S1"),Block([Return(Id("s"))]))),VarDecl("a",Id("S1"), None),VarDecl("c",Id("I1"),Id("a")),VarDecl("d",Id("I2"),Id("a"))])
        """
type S1 struct {votien int;}
type S2 struct {votien int;}
type I1 interface {votien1(e, e int) S1;}
type I2 interface {votien1(a int, b float) S1;}

func (s S1) votien1(a, b int) S1 {return s;}

var a S1;
var c I1 = a;
var d I2 = a;
        """
        self.assertTrue(TestChecker.test(input, "Type Mismatch: VarDecl(d,Id(I2),Id(a))\n", 82))

    def test_085(self):
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("v",IntType(), None),ConstDecl("x",None,Id("v")),VarDecl("k",FloatType(),Id("x")),VarDecl("y",BoolType(),Id("x"))]))])
        expect = "Type Mismatch: Id(v)\n"
        self.assertTrue(TestChecker.test(input, expect, 85))
    
    def test_086(self):
        input = Program([FuncDecl("foo",[],VoidType(),Block([If(BooleanLiteral(True), Block([VarDecl("a",FloatType(),FloatLiteral(1.02))]), Block([VarDecl("a",IntType(),FloatLiteral(1.02))]))]))])
        expect = "Type Mismatch: VarDecl(a,IntType,FloatLiteral(1.02))\n"
        self.assertTrue(TestChecker.test(input, expect, 86))

    def test_091(self):
        input = Program([StructType("TIEN",[("v",IntType())],[]),VarDecl("v",Id("TIEN"), None),FuncDecl("foo",[],VoidType(),Block([ForBasic(IntLiteral(1),Block([VarDecl("a",IntType(),FloatLiteral(1.2))]))]))])
        expect = "Type Mismatch: For(IntLiteral(1),Block([VarDecl(a,IntType,FloatLiteral(1.2))]))\n"
        self.assertTrue(TestChecker.test(input, expect, 91))

    def test_094(self):
        input = Program([StructType("S1",[("v",IntType()),("t",IntType())],[]),VarDecl("a", None,StructLiteral("S1",[("v",IntLiteral(1)),("t",IntLiteral(2))])),VarDecl("b",Id("S1"),Id("a")),VarDecl("c",IntType(),Id("b"))])
        """
type S1 struct {v int; t int;}

var a = S1 {v : 1, t: 2}
var b S1 = a;
var c int = b;
        """
        self.assertTrue(TestChecker.test(input, "Type Mismatch: VarDecl(c,IntType,Id(b))\n", 94))

    def test_096(self):
        """
        var a [2]int = {1,2};
        var c [2]float = a;
        """
        input = Program([VarDecl("a", None,ArrayLiteral([IntLiteral(2)],IntType(),[IntLiteral(1),IntLiteral(2)])),VarDecl("c",ArrayType([IntLiteral(2)],FloatType()),Id("a"))])
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 96))

    def test_101(self):
        input = Program([VarDecl("a",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("b", None,ArrayCell(Id("a"),[IntLiteral(1),IntLiteral(2)])),VarDecl("c",IntType(),Id("b")),VarDecl("d",ArrayType([IntLiteral(1)],StringType()),Id("b"))])
        """
var a [2][3] int;
var b = a[1][2];
var c int = b;
var d [1] string = b;
        
        """
        self.assertTrue(TestChecker.test(input, "Type Mismatch: VarDecl(d,ArrayType(StringType,[IntLiteral(1)]),Id(b))\n", 101))

    def test_102(self):
        input = Program([VarDecl("a",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("b", None,ArrayCell(Id("a"),[IntLiteral(1)])),VarDecl("c",ArrayType([IntLiteral(2)],IntType()),Id("b")),VarDecl("d",ArrayType([IntLiteral(1)],StringType()),Id("b"))])
        expect = "Type Mismatch: VarDecl(c,ArrayType(IntType,[IntLiteral(2)]),Id(b))\n"
        self.assertTrue(TestChecker.test(input, expect, 102))

#     def test_105(self):
#         input = Program([StructType("S1",[("v",IntType()),("x",Id("S1"))],[]),VarDecl("b",Id("S1"), None),VarDecl("c", None,FieldAccess(FieldAccess(Id("b"),"x"),"v")),VarDecl("d", None,FieldAccess(Id("c"),"x"))])
#         """
# type S1 struct {v int; x S1;}
# var b S1;
# var c = b.x.v;
# var d = c.x;
#         """
#         self.assertTrue(TestChecker.test(input, "Type Mismatch: FieldAccess(Id(c),x)\n", 105))

    def test_107(self):
        """
        type S1 struct {votien int;}
        type I1 interface {votien();}
        var a I1;
        var c I1 = nil;
        var d S1 = nil;
        func foo(){
            c := a;
            a := nil;
        }

        var e int = nil;
        :return:
        """
        input = Program([
            StructType("S1",[("votien",IntType())],[]),
            InterfaceType("I1",[Prototype("votien",[],VoidType())]),
            VarDecl("a",Id("I1"), None),
            VarDecl("c",Id("I1"),NilLiteral()),
            VarDecl("d",Id("S1"),NilLiteral()),
            FuncDecl("foo",[],VoidType(),Block([
                Assign(Id("c"),Id("a")),
                Assign(Id("a"),NilLiteral())])),
            VarDecl("e",IntType(),NilLiteral())])
        self.assertTrue(TestChecker.test(input, "Type Mismatch: VarDecl(e,IntType,Nil)\n", 107))

    def test_111(self):
        input = Program([VarDecl("a", None,BinaryOp("+", IntLiteral(1), FloatLiteral(2.0))),VarDecl("b", None,BinaryOp("+", IntLiteral(1), IntLiteral(1))),FuncDecl("foo",[],IntType(),Block([Return(Id("b")),Return(Id("a"))]))])
        """
var a = 1 + 2.0;
var b = 1 + 1;
func foo() int {
    return b;
    return a;
}
        """
        self.assertTrue(TestChecker.test(input, "Type Mismatch: Return(Id(a))\n", 111))

    def test_115(self):
        input = Program([VarDecl("a",IntType(),BinaryOp("%", IntLiteral(1), IntLiteral(2))),VarDecl("b",IntType(),BinaryOp("%", IntLiteral(1), FloatLiteral(2.0)))])
        expect = "Type Mismatch: BinaryOp(IntLiteral(1),%,FloatLiteral(2.0))\n"
        self.assertTrue(TestChecker.test(input, expect, 115))

    def test_116(self):
        input = Program([VarDecl("a",BoolType(),BinaryOp("||", BinaryOp("&&", BooleanLiteral(True), BooleanLiteral(False)), BooleanLiteral(True))),VarDecl("b",BoolType(),BinaryOp("&&", BooleanLiteral(True), IntLiteral(1)))])
        """
var a boolean = true && false || true;
var b boolean = true && 1;
        """
        self.assertTrue(TestChecker.test(input, "Type Mismatch: BinaryOp(BooleanLiteral(true),&&,IntLiteral(1))\n", 116))

    def test_117(self):
        input = Program([VarDecl("a",BoolType(),BinaryOp(">", IntLiteral(1), IntLiteral(2))),VarDecl("b",BoolType(),BinaryOp("<", FloatLiteral(1.0), FloatLiteral(2.0))),VarDecl("c",BoolType(),BinaryOp("==", StringLiteral("\"1\""), StringLiteral("\"2\""))),VarDecl("d",BoolType(),BinaryOp(">", IntLiteral(1), FloatLiteral(2.0)))])
        """
var a boolean = 1 > 2;
var b boolean = 1.0 < 2.0;
var c boolean = "1" == "2";
var d boolean = 1 > 2.0;
        """
        self.assertTrue(TestChecker.test(input, "Type Mismatch: BinaryOp(IntLiteral(1),>,FloatLiteral(2.0))\n", 117))

    def test_118(self):
        input = Program([VarDecl("a",BoolType(),BinaryOp(">=", IntLiteral(1), IntLiteral(2))),VarDecl("b",BoolType(),BinaryOp("<=", FloatLiteral(1.0), FloatLiteral(2.0))),VarDecl("c",BoolType(),BinaryOp("!=", StringLiteral("\"1\""), StringLiteral("\"2\""))),VarDecl("d",BoolType(),BinaryOp(">", IntLiteral(1), BooleanLiteral(True)))])
        """
var a boolean = 1 >= 2;
var b boolean = 1.0 <= 2.0;
var c boolean = "1" != "2";
var d boolean = 1 > true;
        """
        self.assertTrue(TestChecker.test(input, "Type Mismatch: BinaryOp(IntLiteral(1),>,BooleanLiteral(true))\n", 118))

    def test_120(self):
        input = Program([FuncDecl("foo",[],VoidType(),Block([ForStep(VarDecl("i",IntType(),IntLiteral(1)),BinaryOp("<", Id("i"), IntLiteral(10)),Assign(Id("i"),FloatLiteral(1.0)),Block([Return(None)]))]))])
        """
func foo(){
    for var i int = 1; i < 10; i := 1.0 {
        return;
    }
}
        """
        self.assertTrue(TestChecker.test(input, "Type Mismatch: Assign(Id(i),FloatLiteral(1.0))\n", 120))

    def test_121(self):
        input = Program([FuncDecl("foo",[],VoidType(),Block([ForStep(VarDecl("i",IntType(),IntLiteral(1)),BinaryOp("<", Id("a"), IntLiteral(10)),Assign(Id("i"),FloatLiteral(1.0)),Block([VarDecl("a", None,IntLiteral(1))]))]))])
        """
func foo(){
    for var i int = 1; a < 10; i := 1.0 {
        var a = 1;
    }
}
        """
        self.assertTrue(TestChecker.test(input, "Undeclared Identifier: a\n", 116))

    def test_129(self):
        input = Program([FuncDecl("foo",[ParamDecl("a",IntType())],IntType(),Block([Return(IntLiteral(1))])),VarDecl("a",IntType(),FuncCall("foo",[BinaryOp("+", IntLiteral(1), IntLiteral(1))])),VarDecl("b", None,FuncCall("foo",[FloatLiteral(1.0)]))])
        """
func foo(a int) int {return 1;}

var a int = foo(1 + 1);
var b = foo(1.0);
        """
        self.assertTrue(TestChecker.test(input, "Type Mismatch: FuncCall(foo,[FloatLiteral(1.0)])\n", 129))
    
    def test_128(self):
        input = Program([FuncDecl("foo",[],IntType(),Block([Return(IntLiteral(1))])),VarDecl("a",FloatType(),FuncCall("foo",[BinaryOp("+", IntLiteral(1), IntLiteral(1))]))])
        """
func foo() int {return 1;}

var a float = foo(1 + 1);
        """
        self.assertTrue(TestChecker.test(input, "Type Mismatch: FuncCall(foo,[BinaryOp(IntLiteral(1),+,IntLiteral(1))])\n", 129))

    def test_130(self):
        input = Program([StructType("S1",[("vo",IntType())],[]),InterfaceType("I1",[Prototype("votien",[],IntType())]),MethodDecl("s",Id("S1"),FuncDecl("votien",[],IntType(),Block([Return(IntLiteral(1))]))),VarDecl("i",Id("I1"), None),VarDecl("s",Id("S1"), None),VarDecl("a",IntType(),MethCall(Id("i"),"votien",[])),VarDecl("b",IntType(),MethCall(Id("s"),"votien",[])),VarDecl("c",IntType(),MethCall(Id("a"),"votien",[]))])
        """
type S1 struct {vo int;}
type I1 interface {votien() int;}
func (s S1) votien() int {return 1;}

var i I1;
var s S1;
var a int = i.votien();
var b int = s.votien();
var c int = a.votien();
        """
        self.assertTrue(TestChecker.test(input, "Type Mismatch: MethodCall(Id(a),votien,[])\n", 130))

    def test_132(self):
        input = Program([StructType("S1",[("vo",IntType())],[]),InterfaceType("I1",[Prototype("votien",[IntType()],IntType())]),MethodDecl("s",Id("S1"),FuncDecl("votien",[ParamDecl("a",IntType())],IntType(),Block([Return(IntLiteral(1))]))),VarDecl("s",Id("S1"), None),VarDecl("a",IntType(),MethCall(Id("s"),"votien",[IntLiteral(1)])),VarDecl("b",IntType(),MethCall(Id("s"),"votien",[FloatLiteral(1.0)]))])
        """
type S1 struct {vo int;}
type I1 interface {votien(a int) int;}
func (s S1) votien( a int) int {return 1;}

var s S1;
var a int = s.votien(1);
var b int = s.votien(1.0);
        """
        self.assertTrue(TestChecker.test(input, "Type Mismatch: MethodCall(Id(s),votien,[FloatLiteral(1.0)])\n", 132))

    def test_136(self):
        input = Program([FuncDecl("foo",[],IntType(),Block([Return(IntLiteral(1))])),FuncDecl("votien",[],IntType(),Block([Return(FuncCall("votien",[])),FuncCall("foo",[])]))])
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 136)) 

    def test_139(self):
        input = Program([StructType("Person",[("name",StringType()),("age",IntType())],[]),FuncDecl("votien",[],VoidType(),Block([VarDecl("person", None,StructLiteral("Person",[("name",StringLiteral("\"Alice\"")),("age",IntLiteral(30))])),Assign(FieldAccess(Id("person"),"name"),StringLiteral("\"John\"")),Assign(FieldAccess(Id("person"),"age"),IntLiteral(30)),FuncCall("putStringLn",[FieldAccess(Id("person"),"name")]),FuncCall("putStringLn",[MethCall(Id("person"),"Greet",[])])])),MethodDecl("p",Id("Person"),FuncDecl("Greet",[],StringType(),Block([Return(BinaryOp("+", StringLiteral("\"Hello, \""), FieldAccess(Id("p"),"name")))])))])
        """
type Person struct {
    name string ;
    age int ;
}

func  votien()  {
    var person = Person{name: "Alice", age: 30}
    person.name := "John";
    person.age := 30;
    putStringLn(person.name)
    putStringLn(person.Greet())
}

func (p Person) Greet() string {
return "Hello, " + p.name
}
        """
        self.assertTrue(TestChecker.test(input, "", 139))

    def test_143(self):
        input =  """
var a TIEN;
func foo() TIEN {
    return a;
    return TIEN;
}
struct TIEN {int tien;}
"""
        input = Program([VarDecl("a",Id("TIEN"), None),FuncDecl("foo",[],Id("TIEN"),Block([Return(Id("a")),Return(Id("TIEN"))])),StructType("TIEN",[("tien",IntType())],[])])
        expect = "Type Mismatch: Id(TIEN)\n"
        self.assertTrue(TestChecker.test(input, expect, 143))

    def test_145(self):
        input = Program([VarDecl("a", None,IntLiteral(1)),FuncDecl("foo",[],FloatType(),Block([Return(ArrayCell(ArrayLiteral([IntLiteral(2)],IntType(),[IntLiteral(1),IntLiteral(2)]),[Id("a")]))]))])
        """
var a = 1;
func foo() float {
    return [2] int {1, 2}[a];
}
        """
        self.assertTrue(TestChecker.test(input, "Type Mismatch: Return(ArrayCell(ArrayLiteral([IntLiteral(2)],IntType,[IntLiteral(1),IntLiteral(2)]),[Id(a)]))\n", 145))

    def test_149(self):
        input = Program([FuncDecl("putLn",[],VoidType(),Block([Return(None)]))])
        """
func putLn() {return ;}
        """
        self.assertTrue(TestChecker.test(input, "Redeclared Function: putLn\n", 149))

    def test_151(self):
        input = Program([StructType("putLn",[("a",IntType())],[])])
        """
type putLn struct {a int;};
        """
        self.assertTrue(TestChecker.test(input, "Redeclared Type: putLn\n", 151))

    def test_153(self):
        input = Program([VarDecl("a",IntType(),FuncCall("getBool",[]))])
        """
var a int = getBool();
        """
        self.assertTrue(TestChecker.test(input, "Type Mismatch: VarDecl(a,IntType,FuncCall(getBool,[]))\n", 149))

    def test_154(self):
        input = Program([FuncDecl("foo",[],VoidType(),Block([FuncCall("putFloat",[FuncCall("getInt",[])])]))])
        """
func foo() {
    putFloat(getInt());
}
        """
        self.assertTrue(TestChecker.test(input, "Type Mismatch: FuncCall(putFloat,[FuncCall(getInt,[])])\n", 154))

    def test_158(self):
        input = Program([FuncDecl("foo",[],ArrayType([IntLiteral(2)],FloatType()),Block([Return(ArrayLiteral([IntLiteral(2)],FloatType(),[FloatLiteral(1.0),FloatLiteral(2.0)])),Return(ArrayLiteral([IntLiteral(2)],IntType(),[IntLiteral(1),IntLiteral(2)]))]))])
        """
func foo() [2] float {
    return [2] float {1.0, 2.0};
    return [2] int {1, 2};
}
        """
        self.assertTrue(TestChecker.test(input, "Type Mismatch: Return(ArrayLiteral([IntLiteral(2)],IntType,[IntLiteral(1),IntLiteral(2)]))\n", 158))

    def test_164(self):
        input = Program([StructType("TIEN",[("a",ArrayType([IntLiteral(2)],IntType()))],[]),InterfaceType("VO",[Prototype("foo",[],IntType())]),MethodDecl("v",Id("TIEN"),FuncDecl("foo",[],IntType(),Block([Return(IntLiteral(1))]))),FuncDecl("foo",[ParamDecl("a",Id("VO"))],VoidType(),Block([VarDecl("b", None,NilLiteral()),FuncCall("foo",[NilLiteral()])]))])
        """
type TIEN struct {a [2]int;} 
type VO interface {foo() int;}

func (v TIEN) foo() int {return 1;}

func foo(a VO) {
    var b = nil;
    foo(nil)
}
        """
        self.assertTrue(TestChecker.test(input, "", 149))
        
    def test_165(self):
        input = Program([StructType("TIEN",[("a",ArrayType([IntLiteral(2)],IntType()))],[]),FuncDecl("foo",[],Id("TIEN"),Block([Return(NilLiteral())]))])
        """
type TIEN struct {a [2]int;} 

func foo() TIEN {
    return nil
}
        """
        self.assertTrue(TestChecker.test(input, "", 165))

    def test_167(self):
        input = Program([FuncDecl("foo",[],IntType(),Block([VarDecl("a", None,IntLiteral(1)),If(BinaryOp("<", Id("a"), IntLiteral(3)), Block([VarDecl("a", None,IntLiteral(1))]), If(BinaryOp(">", Id("a"), IntLiteral(2)), Block([VarDecl("a", None,IntLiteral(2))]), None)),Return(Id("a"))]))])
        """
func foo() int {
    var a = 1;
    if (a < 3) {
        var a = 1;
    } else if(a > 2) {
        var a = 2;
    }
    return a;
}
        """
        self.assertTrue(TestChecker.test(input, "", 167))

    def test_169(self):
        input = Program([
            FuncDecl("foo", [], VoidType(), Block([
            VarDecl("a", ArrayType([IntLiteral(5), IntLiteral(6)], IntType()), None),
            VarDecl("b", ArrayType([IntLiteral(2)], FloatType()), None),
            Assign(ArrayCell(Id("b"), [IntLiteral(2)]), ArrayCell(Id("a"), [IntLiteral(2), IntLiteral(3)])),
            Assign(ArrayCell(Id("a"), [IntLiteral(2), IntLiteral(3)]), BinaryOp("+", ArrayCell(Id("b"), [IntLiteral(2)]), IntLiteral(1)))
            ]))
        ])
        self.assertTrue(TestChecker.test(input, """Type Mismatch: Assign(ArrayCell(Id(a),[IntLiteral(2),IntLiteral(3)]),BinaryOp(ArrayCell(Id(b),[IntLiteral(2)]),+,IntLiteral(1)))\n""", 169)) 
#TODO :Error
    def test_174(self):
        input =  """
var A = 1;
type A struct {a int;}
        """
        input = Program([VarDecl("A", None,IntLiteral(1)),StructType("A",[("a",IntType())],[])])
        expect = "Redeclared Type: A\n"
        self.assertTrue(TestChecker.test(input, expect, 174)) 
#TODO :Error
    def test_176(self):
        input =  """
    type A interface {foo();}
    const A = 2;
        """
        input = Program([InterfaceType("A",[Prototype("foo",[],VoidType())]),ConstDecl("A",None,IntLiteral(2))])
        self.assertTrue(TestChecker.test(input, """Redeclared Constant: A\n""", 176))
#TODO :Failures
    def test_181(self):
        input = Program([FuncDecl("foo",[ParamDecl("a",ArrayType([IntLiteral(2)],FloatType()))],VoidType(),Block([FuncCall("foo",[ArrayLiteral([IntLiteral(2)],FloatType(),[FloatLiteral(1.0),FloatLiteral(2.0)])]),FuncCall("foo",[ArrayLiteral([IntLiteral(2)],IntType(),[IntLiteral(1),IntLiteral(2)])])]))])
        self.assertTrue(TestChecker.test(input, """""", 181))
#TODO :Error
    def test_182(self):
        input =  """
type S1 struct {votien int;}
type I1 interface {votien();}

func (s S1) votien() {return;}

var b [2] S1;
var a [2] I1 = b;
        """
        input = Program([StructType("S1",[("votien",IntType())],[]),InterfaceType("I1",[Prototype("votien",[],VoidType())]),MethodDecl("s",Id("S1"),FuncDecl("votien",[],VoidType(),Block([Return(None)]))),VarDecl("b",ArrayType([IntLiteral(2)],Id("S1")), None),VarDecl("a",ArrayType([IntLiteral(2)],Id("I1")),Id("b"))])
        expect = "Redeclared Method: votien\n"
        self.assertTrue(TestChecker.test(input, expect, 182)) 
#TODO :Failures
    def test_183(self):
        input = Program([FuncDecl("votien",[ParamDecl("a",ArrayType([IntLiteral(2)],IntType()))],VoidType(),Block([FuncCall("votien",[ArrayLiteral([IntLiteral(3)],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)])])]))])
        """
func votien(a  [2]int ) {
    votien([3] int {1,2,3})
}
        """
        self.assertTrue(TestChecker.test(input, "", 183))
#TODO :Failures
    def test_184(self):
        input =  """
var a [1 + 9] int;
var b [10] int = a;
        """
        input = Program([VarDecl("a",ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(9))],IntType()), None),VarDecl("b",ArrayType([IntLiteral(10)],IntType()),Id("a"))])
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 184)) 

#TODO :Failures
    def test_186(self):
        input = Program([VarDecl("a",ArrayType([BinaryOp("/", IntLiteral(5), IntLiteral(2))],IntType()), None),VarDecl("b",ArrayType([IntLiteral(2)],IntType()),Id("a"))])
        """
var a [5 / 2] int;
var b [2] int = a;
        """
        self.assertTrue(TestChecker.test(input, "", 186))
#TODO :Failures
    def test_190(self):
        input = Program([ConstDecl("v",None,IntLiteral(3)),ConstDecl("a",None,BinaryOp("+", Id("v"), Id("v"))),VarDecl("b",ArrayType([BinaryOp("+", BinaryOp("*", Id("a"), IntLiteral(2)), Id("a"))],IntType()), None),VarDecl("c",ArrayType([IntLiteral(18)],IntType()),Id("b"))])
        self.assertTrue(TestChecker.test(input, """""", 190))
#TODO :Failures    
    def test_191(self):
        input = Program([ConstDecl("v",None,IntLiteral(3)),VarDecl("c",ArrayType([IntLiteral(3)],IntType()),ArrayLiteral([BinaryOp("*", Id("v"), IntLiteral(1))],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)]))])
        """
const v = 3;
var c [3] int = [v * 1] int {1 , 2, 3};
        """
        self.assertTrue(TestChecker.test(input, "", 191))
#TODO :Failures
    def test_192(self):
        input = Program([ConstDecl("v",None,IntLiteral(3)),ConstDecl("k",None,BinaryOp("+", Id("v"), IntLiteral(1))),FuncDecl("foo",[ParamDecl("a",ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))],IntType()))],VoidType(),Block([FuncCall("foo",[ArrayLiteral([BinaryOp("-", Id("k"), IntLiteral(1))],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)])])]))])
        """
const v = 3;
const k = v + 1;
func foo(a [1 + 2] int) {
    foo([k - 1] int {1,2,3})
} 
        """
        self.assertTrue(TestChecker.test(input, "", 192))
#TODO :Error
    def test_194(self):
        input = Program([StructType("K",[("a",IntType())],[]),MethodDecl("k",Id("K"),FuncDecl("koo",[ParamDecl("a",ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))],IntType()))],VoidType(),Block([Return(None)]))),InterfaceType("H",[Prototype("koo",[ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))],IntType())],VoidType())]),ConstDecl("c",None,IntLiteral(4)),FuncDecl("foo",[],VoidType(),Block([VarDecl("k",Id("H"), None),MethCall(Id("k"),"koo",[ArrayLiteral([BinaryOp("-", Id("c"), IntLiteral(1))],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)])])]))])
        """
type K struct {a int;}
func (k K) koo(a [1 + 2] int) {return;}
type H interface {koo(a [1 + 2] int);}

const c = 4;
func foo() {
    var k H;
    k.koo([c - 1] int {1,2,3})
} 
        """
        self.assertTrue(TestChecker.test(input, "", 192))
#TODO :Error
    def test_195(self):
        input = Program([StructType("K",[("a",IntType())],[]),MethodDecl("k",Id("K"),FuncDecl("koo",[ParamDecl("a",ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))],IntType()))],ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))],IntType()),Block([Return(ArrayLiteral([BinaryOp("*", IntLiteral(3), IntLiteral(1))],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)]))]))),InterfaceType("H",[Prototype("koo",[ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))],IntType())],ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))],IntType()))]),ConstDecl("c",None,IntLiteral(4)),FuncDecl("foo",[],ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))],IntType()),Block([Return(FuncCall("foo",[])),VarDecl("k",Id("K"), None),Return(MethCall(Id("k"),"koo",[ArrayLiteral([BinaryOp("-", Id("c"), IntLiteral(1))],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)])])),VarDecl("h",Id("H"), None),Return(MethCall(Id("h"),"koo",[ArrayLiteral([BinaryOp("-", Id("c"), IntLiteral(1))],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)])]))]))])
        """
type K struct {a int;}
func (k K) koo(a [1 + 2] int) [1 + 2] int {return [3*1] int {1,2,3};}
type H interface {koo(a [1 + 2] int) [1 + 2] int;}

const c = 4;
func foo() [1 + 2] int{
    return foo()
    var k K;
    return k.koo([c - 1] int {1,2,3})
    var h H;
    return h.koo([c - 1] int {1,2,3})
} 
        """
        self.assertTrue(TestChecker.test(input, "", 195))
#TODO :Failures
    def test_196(self):
        input = Program([ConstDecl("a",None,BinaryOp("+", StringLiteral("\"2\""), StringLiteral("\"#\""))),ConstDecl("b",None,BinaryOp("*", Id("a"), IntLiteral(5)))])
        """
const a = "2" + "#";
const b = a * 5;
        """
        self.assertTrue(TestChecker.test(input, "Type Mismatch: BinaryOp(Id(a),*,IntLiteral(5))\n", 196))
#TODO :Failures
    def test_197(self):
        input = Program([VarDecl("v", None,BinaryOp("*", IntLiteral(2), IntLiteral(3))),ConstDecl("a",None,BinaryOp("+", Id("v"), IntLiteral(1))),ConstDecl("b",None,BinaryOp("*", Id("a"), IntLiteral(5))),ConstDecl("c",None,UnaryOp("!",BinaryOp(">", Id("b"), IntLiteral(3))))])
        """
var v = 2 * 3;
const a = v + 1;
const b = a * 5;
const c = ! (b > 3);
        """
        self.assertTrue(TestChecker.test(input, "Type Mismatch: Id(v)\n", 197))

#     def test_198(self):
#         input = Program([VarDecl("a",ArrayType([IntLiteral(2),IntLiteral(3),IntLiteral(4)],IntType()), None),VarDecl("b",ArrayType([IntLiteral(3),IntLiteral(4)],IntType()),ArrayCell(Id("a"),[IntLiteral(1)])),VarDecl("c",ArrayType([IntLiteral(4)],IntType()),ArrayCell(Id("a"),[IntLiteral(1),IntLiteral(1)])),VarDecl("d",IntType(),ArrayCell(Id("a"),[IntLiteral(1),IntLiteral(1),IntLiteral(1)]))])
#         """
# var a [2][3][4] int;
# var b [3][4] int = a[1];
# var c [4] int = a[1][1];
# var d int = a[1][1][1];
#         """
#         self.assertTrue(TestChecker.test(input, "", 198))
#TODO :Failures
    def test_199(self):
        input = Program([ConstDecl("a",None,IntLiteral(3)),ConstDecl("b",None,UnaryOp("-",Id("a"))),ConstDecl("c",None,UnaryOp("-",Id("b"))),VarDecl("d",ArrayType([Id("c")],IntType()),ArrayLiteral([IntLiteral(3)],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)]))])
        """
const a = 3;
const b = -a;
const c = -b;
var d [c] int = [3] int {1,2,3}
        """
        self.assertTrue(TestChecker.test(input, "", 199))
#TODO :Failures
    def test_202(self):
        input = """
func foo() {
    a := 1;
    var a = 1;
}
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([Assign(Id("a"),IntLiteral(1)),VarDecl("a", None,IntLiteral(1))]))])
        self.assertTrue(TestChecker.test(input, """Redeclared Variable: a\n""", 202))    
#TODO :Failures
    def test_204(self):
        input = Program([ConstDecl("a",None,IntLiteral(1)),FuncDecl("foo",[],VoidType(),Block([Assign(Id("a"),FloatLiteral(1.0))]))])
        """
const a = 1;
func foo() {
    a := 1.;
}
        """
        self.assertTrue(TestChecker.test(input, "Type Mismatch: Assign(Id(a),FloatLiteral(1.0))\n", 204))
#TODO :Failures
    def test_208(self):
        """
func Votien (b int) {
    for var a = 1; c < 1; a += c {
        const c = 2;
    }
}
        """
        input = Program([FuncDecl("Votien",[ParamDecl("b",IntType())],VoidType(),Block([ForStep(VarDecl("a", None,IntLiteral(1)),BinaryOp("<", Id("c"), IntLiteral(1)),Assign(Id("a"),BinaryOp("+", Id("a"), Id("c"))),Block([ConstDecl("c",None,IntLiteral(2))]))]))])
        self.assertTrue(TestChecker.test(input, """Undeclared Identifier: c\n""", 208))
#TODO :Error    
    def test_210(self):
        """
var v TIEN;
func (v TIEN) foo (v int) int {
    return v;
}

type TIEN struct {
    Votien int;
}
        """
        input = Program([VarDecl("v",Id("TIEN"), None),MethodDecl("v",Id("TIEN"),FuncDecl("foo",[ParamDecl("v",IntType())],IntType(),Block([Return(Id("v"))]))),StructType("TIEN",[("Votien",IntType())],[])])
        self.assertTrue(TestChecker.test(input, "", 210))
#[DONE]TODO :Error
    def test_212(self):
        input = Program([MethodDecl("v",Id("TIEN"),FuncDecl("Votien",[],VoidType(),Block([Return(None)]))),StructType("TIEN",[("Votien",IntType())],[])])
        """
func (v TIEN) Votien () {return ;}
type TIEN struct {
    Votien int;
}
        """
        self.assertTrue(TestChecker.test(input, "Redeclared Method: Votien\n", 212))
#[DONE] TODO :Error
    def test_216(self):
        """
func (v TIEN) VO () {return ;}
func (v TIEN) Tien () {return ;}
type TIEN struct {
    Votien int;
    Tien int;
}
        """
        input = Program([MethodDecl("v",Id("TIEN"),FuncDecl("VO",[],VoidType(),Block([Return(None)]))),MethodDecl("v",Id("TIEN"),FuncDecl("Tien",[],VoidType(),Block([Return(None)]))),StructType("TIEN",[("Votien",IntType()),("Tien",IntType())],[])])
        self.assertTrue(TestChecker.test(input, """Redeclared Method: Tien\n""", 216))
#TODO :Failures
    def test_221(self):
        input = Program([VarDecl("a", None,IntLiteral(1)),FuncDecl("foo",[],VoidType(),Block([Assign(Id("a"),IntLiteral(3)),VarDecl("a", None,FloatLiteral(1.0)),ForStep(VarDecl("a", None,IntLiteral(1)),BinaryOp(">", Id("a"), IntLiteral(1)),Assign(Id("a"),IntLiteral(1)),Block([Return(None)]))]))])
        """
var a = 1;
func foo() {
    a := 3;
    var a = 1.0
    for var a = 1; a > 1; a := 1 {
        return
    }
}
        """
        self.assertTrue(TestChecker.test(input, "", 221))
#[DONE] TODO :Failures
    def test_228(self):
        input = """
func foo() int {
    const foo = 1;
    return foo()
}
        """
        input = Program([FuncDecl("foo",[],IntType(),Block([ConstDecl("foo",None,IntLiteral(1)),Return(FuncCall("foo",[]))]))])
        self.assertTrue(TestChecker.test(input, """Undeclared Function: foo\n""", 228))