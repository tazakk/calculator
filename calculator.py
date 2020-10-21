#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 14:04:44 2020

@author: zakk
"""

import numpy as np

class calculator:
    def __init__(self):
        print "Welcome to the Python Calculator."
        print "Input must be properly formatted."
        print "Handles +, -, *, /, ^, sin, cos, tan, cot, ln, and log (base 10)."
        print "Can evaluate formulas with parenthesis."
    
    def get_input(self):
        formula = raw_input("Enter your formula:")
        return formula
    
    def parse_number(self, formula):
        i = 0
        num = ""
        while formula[i].isdigit() or formula[i] == '.':
            num += formula[i]
            i += 1
            if i == (len(formula)):
                break
        return num, (i-1)
    
    def parse_alpha(self, formula):
        i = 0
        exp = ""
        while formula[i].isalpha():
            exp += formula[i]
            i += 1
            if i == (len(formula)):
                break
        return exp, (i-1)
    
    def is_float(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False
    
    def to_rpn(self, formula):
        precedence_dict = {'^': 0, '*': 1, '/': 1, '+': 2, '-': 2}    # precedence for each operator
        rpn = []
        operators = []
        right_paren, left_paren = ')', '('
        for i in range(0,len(formula)):
            if formula[i].isdigit() or self.is_float(formula[i]):
                rpn.append(formula[i])
            elif (formula[i] == '+' or formula[i] == '-' or formula[i] == '*'
                  or formula[i] == '/' or formula[i] == '^'):
                if len(operators) > 0:
                    top = operators[-1]
                    while ((not len(operators) == 0) and ((precedence_dict[formula[i]] > precedence_dict[top]) or 
                            ((precedence_dict[formula[i]] == precedence_dict[top]) and not (formula[i] == '^'))) and not top == left_paren):
                        rpn.append(operators.pop())
                operators.append(formula[i])
            elif formula[i] == left_paren:
                operators.append(formula[i])
            elif formula[i] == right_paren:
                top = operators[-1]
                while (not top == left_paren):
                    rpn.append(operators.pop())
                if top == left_paren:
                    operators.pop()
                else:
                    print "Error: mismatched parentheses."
                    return -1
            elif formula[i] == "sin":
                operators.append(formula[i])
            elif formula[i] == "cos":
                operators.append(formula[i])
            elif formula[i] == "tan":
                operators.append(formula[i])
            elif formula[i] == "cot":
                operators.append(formula[i])
            elif formula[i] == "ln":
                operators.append(formula[i])
            elif formula[i] == "log":
                operators.append(formula[i])
        while len(operators) > 0:
            rpn.append(operators.pop())
        print "The formula converted to Reverse Polish Notation:", rpn
        return rpn
    
    def is_operator(self, val):
        if val == '+' or val == '-':
            return True
        if val == '*' or val == '/':
            return True
        if val == '^':
            return True
        return False
    
    def parse_equation(self, formula):
        exp = []
        i = 0
        while i < len(formula):
            if formula[i].isdigit():
                val, cnt = self.parse_number(formula[i:])
                exp.append(val)
                i += int(cnt) + 1
            else:
                if formula[i].isalpha():
                    val, cnt = self.parse_alpha(formula[i:])
                    exp.append(val)
                    i += int(cnt) + 1
                elif formula[i] == '+':
                    exp.append('+')
                    i += 1
                elif formula[i] == '-':
                    if i == 0 or (formula[i-1].isalpha() or formula[i-1] == ')' or formula[i-1] == '(' or self.is_operator(formula[i-1])):
                        val, cnt = self.parse_number(formula[i+1:])
                        val = "-" + val
                        exp.append(val)
                        i += int(cnt) + 2
                    else:
                        exp.append('-')
                        i += 1
                elif formula[i] == '*':
                    exp.append('*')
                    i += 1
                elif formula[i] == '/':
                    exp.append('/')
                    i += 1
                elif formula[i] == '^':
                    exp.append('^')
                    i += 1
                elif formula[i] == '(':
                    exp.append('(')
                    i += 1
                elif formula[i] == ')':
                    exp.append(')')
                    i += 1
                else:
                    print "Error: Invalid input."
                    return
        return exp
    
    def evaluate_expression(self, rpn):
        operands = []
        for i in range(0, len(rpn)):
            if rpn[i].isdigit() or self.is_float(rpn[i]):
                operands.append(rpn[i])
            else:
                operator = rpn[i]
                if operator == '+':
                    y = float(operands.pop())
                    x = float(operands.pop())
                    part = float(x + y)
                    operands.append(part)
                elif operator == '-':
                    y = float(operands.pop())
                    x = float(operands.pop())
                    part = float(x - y)
                    operands.append(part)
                elif operator == '*':
                    y = float(operands.pop())
                    x = float(operands.pop())
                    part = float(x * y)
                    operands.append(part)
                elif operator == '/':
                    y = float(operands.pop())
                    x = float(operands.pop())
                    part = float(x / y)
                    operands.append(part)
                elif operator == '^':
                    y = float(operands.pop())
                    x = float(operands.pop())
                    part = float(x**y)
                    operands.append(part)
                elif operator == "sin":
                    x = float(operands.pop())
                    part = float(np.sin(x))
                    operands.append(part)
                elif operator == "cos":
                    x = float(operands.pop())
                    part = float(np.cos(x))
                    operands.append(part)
                elif operator == "tan":
                    x = float(operands.pop())
                    part = float(np.tan(x))
                    operands.append(part)
                elif operator == "cot":
                    x = float(operands.pop())
                    part = float(1.0/np.tan(x))
                    operands.append(part)
                elif operator == "ln":
                    x = float(operands.pop())
                    part = float(np.log(x))
                    operands.append(part)
                elif operator == "log":
                    x = float(operands.pop())
                    part = float(np.log10(x))
                    operands.append(part)
                else:
                    print "Error: Invalid input."
                    return -1
        if len(operands) > 1:
            print "Error: mismatch between operands and operators."
            return -1
        else:
            return float(operands.pop())
            
    
def main():
    my_calc = calculator()
    cont = True
    while cont:
        formula = my_calc.get_input()
        print "Formula:", formula
        print
        exp = my_calc.parse_equation(formula)
        print "Parsed:", exp
        print
        rpn = my_calc.to_rpn(exp)
        print
        print my_calc.evaluate_expression(rpn)
        print 
        y = raw_input("Do you wish to continue? Type 'y' for yes.")
        cont = (y == 'y')
    print "Goodbye."
    
main()