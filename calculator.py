#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 14:04:44 2020

CS 480 - Lab 3

This is my implementation of a calculator that can handle basic arithmetic,
logarithmic, and trigonometric functions with operator precedence and parentheses.

@author: Zachary Dehaan
"""

import numpy as np

# The class that contains all pertinent methods
class calculator:
    # "Initializes" the calculator and prints some introductions
    def __init__(self):
        print "================================================================="
        print "Welcome to the Python Calculator."
        print
        print "> Input must be properly formatted."
        print "> Handles +, -, *, /, ^, sin, cos, tan, cot, ln, and log (base 10)."
        print "> Can evaluate formulas with parenthesis."
        print "> Enter equation when prompted and click enter to calculate."
        print "> All answers are in Radians."
        print 
        print "============================BEGIN================================"
        print
    
    # Asks for the formula from the user and returns it as a string
    def get_input(self):
        formula = raw_input("Enter your formula:\n\n")
        return formula
    
    # Parses a number from a string
    #
    # Called whenever a single digit is reached. Loops until the current character
    # is not a digit or a decimal. Ensures we can use numbers with more than one
    # digit and numbers that are floating-point.
    # Returns the full number as a single string and a count of how many indexes
    # were taken up by the number in the string. The count is used to increment
    # the counter in parse_equation in order to prevent multiplie processing of
    # a single element.
    def parse_number(self, formula):
        i = 0
        num = ""
        if len(formula) > 0:
            while formula[i].isdigit() or formula[i] == '.':
                num += formula[i]
                i += 1
                if i == (len(formula)):
                    break
            return num, (i-1)
        else:
            print "Error: Invalid input."
            return -1
    
    # Parses a function from a string
    #
    # Called whenever an alphabetic character is reached. Loops until the current
    # character is not alphabetic. Ensures that we pull the entire function name
    # without grabbing any numbers or operators.
    # Returns the function as a single string and a count of how many indexes were
    # taken up by the function in the string. The count is used to increment the
    # counter in parse_equation in order to prevent multiple processing of a single
    # element.
    def parse_alpha(self, formula):
        i = 0
        exp = ""
        while formula[i].isalpha():
            exp += formula[i]
            i += 1
            if i == (len(formula)):
                break
        return exp, (i-1)
    
    # Helper method that tests whether a given element is a float.
    #
    # Used to determine if a number in the parsed equation is a float. Cannot use
    # the built-in method isdigit() since it only evaluates to true for integers.
    # Returns true if the element is a floating-point number.
    def is_float(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False
    
    # Converts the parsed formula to Reverse Polish Notation using the Shunting-yard
    # algorithm. Pseudocode was found on wikipedia.org and was implemented in this method.
    #
    # Considers operator precedence, left/right associativity, and parentheses.
    # Returns the formula converted to RPN.
    def to_rpn(self, formula):
        precedence_dict = {'^': 0, '(':-1, '*': 1, '/': 1, '+': 2, '-': 2, "sin":-1, "cos":-1,
                           "tan":-1, "cot":-1, "ln":-1, "log":-1}    # precedence for each operator
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
                    while ((not len(operators) == 0) and ((precedence_dict[formula[i]] > precedence_dict[top]) or ((precedence_dict[formula[i]] == precedence_dict[top]) and not (formula[i] == '^'))) and not top == left_paren):
                        rpn.append(operators.pop())
                        if not len(operators) == 0:
                            top = operators[-1]
                operators.append(formula[i])
            elif formula[i] == left_paren:
                operators.append(formula[i])
            elif formula[i] == right_paren:
                top = operators[-1]
                while (not top == left_paren):
                    rpn.append(operators.pop())
                    top = operators[-1]
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
        return rpn
    
    # Helper method that determines whether an element is an operator.
    #
    # Returns true if the element is an operator.
    def is_operator(self, val):
        if val == '+' or val == '-':
            return True
        if val == '*' or val == '/':
            return True
        if val == '^':
            return True
        return False
    
    # Parses the equation into its elements.
    #
    # Ex: "123+4" => '1','2','3','+','4' => '123','+','4'
    # Deciphers whether a "-" is a subraction or a negative.
    # Returns the parsed equation.
    def parse_equation(self, formula):
        exp = []
        i = 0
        while i < len(formula):
            if formula[i].isdigit() or formula[i] == '.':
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
                    if (i == 0 and not i == len(formula)-1) or (formula[i-1].isalpha() or formula[i-1] == '(' or self.is_operator(formula[i-1])):
                        val, cnt = self.parse_number(formula[i+1:])
                        if val == "":
                            val = "-" + val + "1"
                        elif val == -1:
                            return
                        else:
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
                    if i == 0:
                        exp.append('(')
                    elif (not formula[i-1] == '(') and (formula[i-1].isdigit() or (self.is_operator(formula[i-1] and not formula[i-1] == '*') or (exp[-1].isdigit() or self.is_float(exp[-1])))):
                        exp.append('*')
                        exp.append('(')
                    else:
                        exp.append('(')
                    i += 1
                elif formula[i] == ')':
                    exp.append(')')
                    i += 1
                else:
                    print "Error: Invalid input."
                    return
        return exp
    
    # Evaluates an expression that is written in Reverse Polish Notation.
    #
    # Utilizes a stack to hold operands. When an operator is reached, one or
    # two operands are popped off the stack and the operator is applied to them.
    # Then the result of that calculation is popped back onto the operator stack
    # and the process continues until there are no more operators. If 
    def evaluate_expression(self, rpn):
        operands = []
        for i in range(0, len(rpn)):
            if rpn[i].isdigit() or self.is_float(rpn[i]):
                operands.append(rpn[i])
            else:
                operator = rpn[i]
                if operator == '+':
                    try:
                        y = float(operands.pop())
                        x = float(operands.pop())
                    except IndexError:
                        print "Error: Invalid input."
                        return -1
                    part = float(x + y)
                    operands.append(part)
                elif operator == '-':
                    try:
                        y = float(operands.pop())
                        x = float(operands.pop())
                    except IndexError:
                        print "Error: Invalid input."
                        return -1
                    part = float(x - y)
                    operands.append(part)
                elif operator == '*':
                    try:
                        y = float(operands.pop())
                        x = float(operands.pop())
                    except IndexError:
                        print "Error: Invalid input."
                        return -1
                    part = float(x * y)
                    operands.append(part)
                elif operator == '/':
                    try:
                        y = float(operands.pop())
                        x = float(operands.pop())
                    except IndexError:
                        print "Error: Invalid input."
                        return -1
                    part = float(x / y)
                    operands.append(part)
                elif operator == '^':
                    try:
                        y = float(operands.pop())
                        x = float(operands.pop())
                    except IndexError:
                        print "Error: Invalid input."
                        return -1
                    part = float(x**y)
                    operands.append(part)
                elif operator == "sin":
                    try:
                        x = float(operands.pop())
                    except IndexError:
                        print "Error: Invalid input."
                        return -1
                    part = float(np.sin(x))
                    operands.append(part)
                elif operator == "cos":
                    try:
                        x = float(operands.pop())
                    except IndexError:
                        print "Error: Invalid input."
                        return -1
                    part = float(np.cos(x))
                    operands.append(part)
                elif operator == "tan":
                    try:
                        x = float(operands.pop())
                    except IndexError:
                        print "Error: Invalid input."
                        return -1
                    part = float(np.tan(x))
                    operands.append(part)
                elif operator == "cot":
                    try:
                        x = float(operands.pop())
                    except IndexError:
                        print "Error: Invalid input."
                        return -1
                    part = float(1.0/np.tan(x))
                    operands.append(part)
                elif operator == "ln":
                    try:
                        x = float(operands.pop())
                    except IndexError:
                        print "Error: Invalid input."
                        return -1
                    part = float(np.log(x))
                    operands.append(part)
                elif operator == "log":
                    try:
                        x = float(operands.pop())
                    except IndexError:
                        print "Error: Invalid input."
                        return -1
                    part = float(np.log10(x))
                    operands.append(part)
                else:
                    print "Error: Invalid input."
                    return -1
        if len(operands) > 1:
            print "Error: mismatch between operands and operators."
            return -1
        else:
            print "\nThe answer is", float(operands[0])
            return float(operands.pop())
            
    
def main():
    my_calc = calculator()
    cont = True
    err = False
    while cont:
        print "=== New calculation ==="
        formula = my_calc.get_input()
        try:
            exp = my_calc.parse_equation(formula)
        except:
            err = True
        if not err:
            try:
                rpn = my_calc.to_rpn(exp)
            except:
                err = True
            if not err:
                try:
                    my_calc.evaluate_expression(rpn)
                except:
                    err = True
        if err:
            print "Error: Invalid input."
        y = raw_input("Do you wish to continue? (Y/N): ")
        cont = (y == 'y' or y == 'Y')
        print
    print "Goodbye."
    
main()