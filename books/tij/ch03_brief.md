# 3. Operators (printed p63-92)


<!--p85-->
Operators At the lowest level, data in Java is manipulated using operators. Because Java was inherited from C++, most of these operators will be familiar to C and C++ programmers. Java has also added some improvements and simplifications. If you’re familiar with C or C++ syntax, you can skim through this chapter and the next, looking for places where Java is different from those languages. However, if you find yourself floundering a bit in these two chapters, make sure you go through the multimedia seminar Thinking in C, freely downloadable from www.MindView.net. It contains audio lectures, slides, exercises, and solutions specifically designed to bring you up to speed with the fundamentals necessary to learn Java. Simpler print statements In the previous chapter, you were introduced to the Java print statement:
```java
System.out.println("Rather a lot to type");
```
You may observe that this is not only a lot to type (and thus many redundant tendon hits), but also rather noisy to read. Most languages before and after Java have taken a much simpler approach to such a commonly used statement. The Access Control chapter introduces the concept of the static import that was added to Java SE5, and creates a tiny library to simplify writing print statements. However, you don’t need to know those details in order to begin using that library. We can rewrite the program from the last chapter using this new library:
```java
//: operators/HelloDate.java
import java.util.*;
import static net.mindview.util.Print.*;
public class HelloDate {
public static void main(String[] args) {
print("Hello, it’s: ");
print(new Date());
}
} /* Output: (55% match)
Hello, it’s:
Wed Oct 05 14:39:05 MDT 2005
*///:~
```

<!--p86-->
The results are much cleaner. Notice the insertion of the static keyword in the second import statement. In order to use this library, you must download this book’s code package from www.MindView.net or one of its mirrors. Unzip the code tree and add the root directory of that code tree to your computer’s CLASSPATH environment variable. (You’ll eventually get a full introduction to the classpath, but you might as well get used to struggling with it early. Alas, it is one of the more common battles you will have with Java.) Although the use of net.mindview.util.Print nicely simplifies most code, it is not justifiable everywhere. If there are only a small number of print statements in a program, I forego the import and write out the full System.out.println( ). Exercise 1: (1) Write a program that uses the “short” and normal form of print statement. Using Java operators An operator takes one or more arguments and produces a new value. The arguments are in a different form than ordinary method calls, but the effect is the same. Addition and unary plus (+), subtraction and unary minus (-), multiplication (*), division (/), and assignment (=) all work much the same in any programming language. All operators produce a value from their operands. In addition, some operators change the value of an operand. This is called a side effect. The most common use for operators that modify their operands is to generate the side effect, but you should keep in mind that the value produced is available for your use, just as in operators without side effects. Almost all operators work only with primitives. The exceptions are ‘=‘, ‘==‘ and ‘!=‘, which work with all objects (and are a point of confusion for objects). In addition, the String class supports ‘+’ and ‘+=‘. Precedence Operator precedence defines how an expression evaluates when several operators are present. Java has specific rules that determine the order of evaluation. The easiest one to remember is that multiplication and division happen before addition and subtraction. Programmers often forget the other precedence rules, so you should use parentheses to make the order of evaluation explicit. For example, look at statements (1) and (2):
```java
//: operators/Precedence.java
public class Precedence {
public static void main(String[] args) {
int x = 1, y = 2, z = 3;
int a = x + y - 2/2 + z; // (1)
int b = x + (y - 2)/(2 + z); // (2)
System.out.println("a = " + a + " b = " + b);
}
} /* Output:
a = 5 b = 1
*///:~
```

<!--p87-->
These statements look roughly the same, but from the output you can see that they have very different meanings which depend on the use of parentheses. Notice that the System.out.println( ) statement involves the ‘+’ operator. In this context, ‘+’ means “string concatenation” and, if necessary, “string conversion.” When the compiler sees a String followed by a ‘+’ followed by a non-String, it attempts to convert the non- String into a String. As you can see from the output, it successfully converts from int into String for a and b. Assignment Assignment is performed with the operator =. It means “Take the value of the right-hand side (often called the rvalue) and copy it into the left-hand side (often called the lvalue)”. An rvalue is any constant, variable, or expression that produces a value, but an lvalue must be a distinct, named variable. (That is, there must be a physical space to store the value.) For instance, you can assign a constant value to a variable:
```java
a = 4;
```
but you cannot assign anything to a constant value—it cannot be an lvalue. (You can’t say 4 = a;.) Assignment of primitives is quite straightforward. Since the primitive holds the actual value and not a reference to an object, when you assign primitives, you copy the contents from one place to another. For example, if you say a = b for primitives, then the contents of b are copied into a. If you then go on to modify a, b is naturally unaffected by this modification. As a programmer, this is what you can expect for most situations. When you assign objects, however, things change. Whenever you manipulate an object, what you’re manipulating is the reference, so when you assign “from one object to another,” you’re actually copying a reference from one place to another. This means that if you say c = d for objects, you end up with both c and d pointing to the object that, originally, only d pointed to. Here’s an example that demonstrates this behavior:
```java
//: operators/Assignment.java
// Assignment with objects is a bit tricky.
import static net.mindview.util.Print.*;
class Tank {
int level;
}
public class Assignment {
public static void main(String[] args) {
Tank t1 = new Tank();
Tank t2 = new Tank();
t1.level = 9;
t2.level = 47;
print("1: t1.level: " + t1.level +
", t2.level: " + t2.level);
t1 = t2;
print("2: t1.level: " + t1.level +
", t2.level: " + t2.level);
t1.level = 27;
print("3: t1.level: " + t1.level +
", t2.level: " + t2.level);
}
} /* Output:
1: t1.level: 9, t2.level: 47
2: t1.level: 47, t2.level: 47
3: t1.level: 27, t2.level: 27
*///:~
```

<!--p88-->
The Tank class is simple, and two instances (t1 and t2) are created within main( ). The level field within each Tank is given a different value, and then t2 is assigned to t1, and t1 is changed. In many programming languages you expect t1 and t2 to be independent at all times, but because you’ve assigned a reference, changing the t1 object appears to change the t2 object as well! This is because both t1 and t2 contain the same reference, which is Operators pointing to the same object. (The original reference that was in t1, that pointed to the object holding a value of 9, was overwritten during the assignment and effectively lost; its object will be cleaned up by the garbage collector.) This phenomenon is often called aliasing, and it’s a fundamental way that Java works with objects. But what if you don’t want aliasing to occur in this case? You could forego the assignment and say:
```java
t1.level = t2.level;
```
This retains the two separate objects instead of discarding one and tying t1 and t2 to the same object. You’ll soon realize that manipulating the fields within objects is messy and goes against good object-oriented design principles. This is a nontrivial topic, so you should keep in mind that assignment for objects can add surprises. Exercise 2: (1) Create a class containing a float and use it to demonstrate aliasing. Aliasing during method calls Aliasing will also occur when you pass an object into a method:
```java
//: operators/PassObject.java
// Passing objects to methods may not be
// what you’re used to.
import static net.mindview.util.Print.*;
class Letter {
char c;
}
public class PassObject {
static void f(Letter y) {
y.c = ‘z’;
}
public static void main(String[] args) {
Letter x = new Letter();
x.c = ‘a’;
print("1: x.c: " + x.c);
f(x);
print("2: x.c: " + x.c);
}
} /* Output:
1: x.c: a
2: x.c: z
*///:~
```
In many programming languages, the method f( ) would appear to be making a copy of its argument Letter y inside the scope of the method. But once again a reference is being passed, so the line
```java
y.c = ‘z’;
```

<!--p89-->
is actually changing the object outside of f( ). Aliasing and its solution is a complex issue which is covered in one of the online supplements for this book. However, you should be aware of it at this point so you can watch for pitfalls. Exercise 3: (1) Create a class containing a float and use it to demonstrate aliasing during method calls. Mathematical operators The basic mathematical operators are the same as the ones available in most programming languages: addition (+), subtraction (-), division (/), multiplication (*) and modulus (%, which produces the remainder from integer division). Integer division truncates, rather than rounds, the result. Java also uses the shorthand notation from C/C++ that performs an operation and an assignment at the same time. This is denoted by an operator followed by an equal sign, and is consistent with all the operators in the language (whenever it makes sense). For example, to add 4 to the variable x and assign the result to x, use: x += 4. This example shows the use of the mathematical operators:
```java
//: operators/MathOps.java
// Demonstrates the mathematical operators.
import java.util.*;
import static net.mindview.util.Print.*;
public class MathOps {
public static void main(String[] args) {
// Create a seeded random number generator:
Random rand = new Random(47);
int i, j, k;
// Choose value from 1 to 100:
j = rand.nextInt(100) + 1;
print("j : " + j);
k = rand.nextInt(100) + 1;
print("k : " + k);
i = j + k;
print("j + k : " + i);
i = j - k;
print("j - k : " + i);
i = k / j;
print("k / j : " + i);
i = k * j;
print("k * j : " + i);
i = k % j;
print("k % j : " + i);
j %= k;
print("j %= k : " + j);
// Floating-point number tests:
float u, v, w; // Applies to doubles, too
v = rand.nextFloat();
print("v : " + v);
w = rand.nextFloat();
print("w : " + w);
u = v + w;
print("v + w : " + u);
u = v - w;
print("v - w : " + u);
u = v * w;
print("v * w : " + u);
u = v / w;
print("v / w : " + u);
// The following also works for char,
// byte, short, int, long, and double:
```

<!--p90-->
Operators
```java
u += v;
print("u += v : " + u);
u -= v;
print("u -= v : " + u);
u *= v;
print("u *= v : " + u);
u /= v;
print("u /= v : " + u);
}
} /* Output:
j : 59
k : 56
j + k : 115
j - k : 3
k / j : 0
k * j : 3304
k % j : 56
j %= k : 3
v : 0.5309454
w : 0.0534122
v + w : 0.5843576
v - w : 0.47753322
v * w : 0.028358962
v / w : 9.940527
u += v : 10.471473
u -= v : 9.940527
u *= v : 5.2778773
u /= v : 9.940527
*///:~
```

<!--p91-->
To generate numbers, the program first creates a Random object. If you create a Random object with no arguments, Java uses the current time as a seed for the random number generator, and will thus produce different output for each execution of the program. However, in the examples in this book, it is important that the output shown at the end of the examples be as consistent as possible, so that this output can be verified with external tools. By providing a seed (an initialization value for the random number generator that will always produce the same sequence for a particular seed value) when creating the Random object, the same random numbers will be generated each time the program is executed, so the output is verifiable.1To generate more varying output, feel free to remove the seed in the examples in the book. The program generates a number of different types of random numbers with the Random object simply by calling the methods nextInt( ) and nextFloat( ) (you can also call nextLong( ) or nextDouble( )). The argument to nextInt( ) sets the upper bound on the generated number. The lower bound is zero, which we don’t want because of the possibility of a divide-by-zero, so the result is offset by one. Exercise 4: (2) Write a program that calculates velocity using a constant distance and a constant time. Unary minus and plus operators The unary minus (-) and unary plus (+) are the same operators as binary minus and plus. The compiler figures out which use is intended by the way you write the expression. For instance, the statement 1The number 47 was considered a “magic number” at a college I attended, and it stuck.
```java
x = -a;
```
has an obvious meaning. The compiler is able to figure out:
```java
x = a * -b;
```
but the reader might get confused, so it is sometimes clearer to say:
```java
x = a * (-b);
```
Unary minus inverts the sign on the data. Unary plus provides symmetry with unary minus, although it doesn’t have any effect. Auto increment and decrement Java, like C, has a number of shortcuts. Shortcuts can make code much easier to type, and either easier or harder to read. Two of the nicer shortcuts are the increment and decrement operators (often referred to as the auto-increment and auto-decrement operators). The decrement operator is -- and means “decrease by one unit.” The increment operator is ++ and means “increase by one unit.” If a is an int, for example, the expression ++a is equivalent to (a = a + 1). Increment and decrement operators not only modify the variable, but also produce the value of the variable as a result. There are two versions of each type of operator, often called the prefix and postfix versions. Preincrement means the ++ operator appears before the variable, and post-increment means the ++ operator appears after the variable. Similarly, pre-decrement means the -- operator appears before the variable, and post-decrement means the -- operator appears after the variable. For pre-increment and pre-decrement (i.e., ++a or --a), the operation is performed and the value is produced. For post-increment and post-decrement (i.e., a++ or a--), the value is produced, then the operation is performed. As an example:
```java
//: operators/AutoInc.java
// Demonstrates the ++ and -- operators.
import static net.mindview.util.Print.*;
public class AutoInc {
public static void main(String[] args) {
int i = 1;
print("i : " + i);
print("++i : " + ++i); // Pre-increment
print("i++ : " + i++); // Post-increment
print("i : " + i);
print("--i : " + --i); // Pre-decrement
print("i-- : " + i--); // Post-decrement
print("i : " + i);
}
} /* Output:
i : 1
++i : 2
i++ : 2
i : 3
--i : 2
i-- : 2
i : 1
*///:~
```

<!--p92-->
Operators You can see that for the prefix form, you get the value after the operation has been performed, but with the postfix form, you get the value before the operation is performed. These are the only operators, other than those involving assignment, that have side effects— they change the operand rather than using just its value. The increment operator is one explanation for the name C++, implying “one step beyond C.” In an early Java speech, Bill Joy (one of the Java creators), said that “Java=C++--” (C plus plus minus minus), suggesting that Java is C++ with the unnecessary hard parts removed, and therefore a much simpler language. As you progress in this book, you’ll see that many parts are simpler, and yet in other ways Java isn’t much easier than C++. Relational operators Relational operators generate a boolean result. They evaluate the relationship between the values of the operands. A relational expression produces true if the relationship is true, and false if the relationship is untrue. The relational operators are less than (<), greater than (>), less than or equal to (<=), greater than or equal to (>=), equivalent (==) and not equivalent (!=). Equivalence and nonequivalence work with all primitives, but the other comparisons won’t work with type boolean. Because boolean values can only be true or false, “greater than” and “less than” doesn’t make sense. Testing object equivalence The relational operators == and != also work with all objects, but their meaning often confuses the first-time Java programmer. Here’s an example:
```java
//: operators/Equivalence.java
public class Equivalence {
public static void main(String[] args) {
Integer n1 = new Integer(47);
Integer n2 = new Integer(47);
System.out.println(n1 == n2);
System.out.println(n1 != n2);
}
} /* Output:
false
true
*///:~
```
The statement System.out.println(n1 == n2) will print the result of the boolean comparison within it. Surely the output should be “true” and then “false,” since both Integer objects are the same. But while the contents of the objects are the same, the references are not the same. The operators == and != compare object references, so the output is actually “false” and then “true.” Naturally, this surprises people at first. What if you want to compare the actual contents of an object for equivalence? You must use the special method equals( ) that exists for all objects (not primitives, which work fine with == and !=). Here’s how it’s used:

<!--p93-->
```java
//: operators/EqualsMethod.java
public class EqualsMethod {
public static void main(String[] args) {
Integer n1 = new Integer(47);
Integer n2 = new Integer(47);
System.out.println(n1.equals(n2));
}
} /* Output:
true
*///:~
```
The result is now what you expect. Ah, but it’s not as simple as that. If you create your own class, like this:
```java
//: operators/EqualsMethod2.java
// Default equals() does not compare contents.
class Value {
int i;
}
public class EqualsMethod2 {
public static void main(String[] args) {
Value v1 = new Value();
Value v2 = new Value();
v1.i = v2.i = 100;
System.out.println(v1.equals(v2));
}
} /* Output:
false
*///:~
```
things are confusing again: The result is false. This is because the default behavior of equals( ) is to compare references. So unless you override equals( ) in your new class you won’t get the desired behavior. Unfortunately, you won’t learn about overriding until the Reusing Classes chapter and about the proper way to define equals( ) until the Containers in Depth chapter, but being aware of the way equals( ) behaves might save you some grief in the meantime. Most of the Java library classes implement equals( ) so that it compares the contents of objects instead of their references. Exercise 5: (2) Create a class called Dog containing two Strings: name and says. In main( ), create two dog objects with names “spot” (who says, “Ruff!”) and “scruffy” (who says, “Wurf!”). Then display their names and what they say. Exercise 6: (3) Following Exercise 5, create a new Dog reference and assign it to spot’s object. Test for comparison using == and equals( ) for all references. Logical operators Each of the logical operators AND (&&), OR (||) and NOT (!) produces a boolean value of true or false based on the logical relationship of its arguments. This example uses the relational and logical operators:
```java
//: operators/Bool.java
// Relational and logical operators.
import java.util.*;
import static net.mindview.util.Print.*;
public class Bool {
public static void main(String[] args) {
Random rand = new Random(47);
int i = rand.nextInt(100);
```

<!--p94-->
Operators
```java
int j = rand.nextInt(100);
print("i = " + i);
print("j = " + j);
print("i > j is " + (i > j));
print("i < j is " + (i < j));
print("i >= j is " + (i >= j));
print("i <= j is " + (i <= j));
print("i == j is " + (i == j));
print("i != j is " + (i != j));
// Treating an int as a boolean is not legal Java:
//! print("i && j is " + (i && j));
//! print("i || j is " + (i || j));
//! print("!i is " + !i);
print("(i < 10) && (j < 10) is "
+ ((i < 10) && (j < 10)) );
print("(i < 10) || (j < 10) is "
+ ((i < 10) || (j < 10)) );
}
} /* Output:
i = 58
j = 55
i > j is true
i < j is false
i >= j is true
i <= j is false
i == j is false
i != j is true
(i < 10) && (j < 10) is false
(i < 10) || (j < 10) is false
*///:~
```
You can apply AND, OR, or NOT to boolean values only. You can’t use a non-boolean as if it were a boolean in a logical expression as you can in C and C++. You can see the failed attempts at doing this commented out with a ‘//!’ (this comment syntax enables automatic removal of comments to facilitate testing). The subsequent expressions, however, produce boolean values using relational comparisons, then use logical operations on the results. Note that a boolean value is automatically converted to an appropriate text form if it is used where a String is expected. You can replace the definition for int in the preceding program with any other primitive data type except boolean. Be aware, however, that the comparison of floating point numbers is very strict. A number that is the tiniest fraction different from another number is still “not equal.” A number that is the tiniest bit above zero is still nonzero. Exercise 7: (3) Write a program that simulates coin-flipping. Short-circuiting When dealing with logical operators, you run into a phenomenon called “short-circuiting.” This means that the expression will be evaluated only untilthe truth or falsehood of the entire expression can be unambiguously determined. As a result, the latter parts of a logical expression might not be evaluated. Here’s an example that demonstrates short-circuiting:

<!--p95-->
```java
//: operators/ShortCircuit.java
// Demonstrates short-circuiting behavior
// with logical operators.
import static net.mindview.util.Print.*;
public class ShortCircuit {
static boolean test1(int val) {
print("test1(" + val + ")");
print("result: " + (val < 1));
return val < 1;
}
static boolean test2(int val) {
print("test2(" + val + ")");
print("result: " + (val < 2));
return val < 2;
}
static boolean test3(int val) {
print("test3(" + val + ")");
print("result: " + (val < 3));
return val < 3;
}
public static void main(String[] args) {
boolean b = test1(0) && test2(2) && test3(2);
print("expression is " + b);
}
} /* Output:
test1(0)
result: true
test2(2)
result: false
expression is false
*///:~
```
Each test performs a comparison against the argument and returns true or false. It also prints information to show you that it’s being called. The tests are used in the expression:
```java
test1(0) && test2(2) && test3(2)
```
You might naturally think that all three tests would be executed, but the output shows otherwise. The first test produced a true result, so the expression evaluation continues. However, the second test produced a false result. Since this means that the whole expression must be false, why continue evaluating the rest of the expression? It might be expensive. The reason for shortcircuiting, in fact, is that you can get a potential performance increase if all the parts of a logical expression do not need to be evaluated. Literals Ordinarily, when you insert a literal value into a program, the compiler knows exactly what type to make it. Sometimes, however, the type is ambiguous. When this happens, you must guide the compiler by adding some extra information in the form of characters associated with the literal value. The following code shows these characters:
```java
//: operators/Literals.java
import static net.mindview.util.Print.*;
public class Literals {
public static void main(String[] args) {
int i1 = 0x2f; // Hexadecimal (lowercase)
print("i1: " + Integer.toBinaryString(i1));
int i2 = 0X2F; // Hexadecimal (uppercase)
print("i2: " + Integer.toBinaryString(i2));
int i3 = 0177; // Octal (leading zero)
print("i3: " + Integer.toBinaryString(i3));
char c = 0xffff; // max char hex value
```

<!--p96-->
Operators
```java
print("c: " + Integer.toBinaryString(c));
byte b = 0x7f; // max byte hex value
print("b: " + Integer.toBinaryString(b));
short s = 0x7fff; // max short hex value
print("s: " + Integer.toBinaryString(s));
long n1 = 200L; // long suffix
long n2 = 200l; // long suffix (but can be confusing)
long n3 = 200;
float f1 = 1;
float f2 = 1F; // float suffix
float f3 = 1f; // float suffix
double d1 = 1d; // double suffix
double d2 = 1D; // double suffix
// (Hex and Octal also work with long)
}
} /* Output:
i1: 101111
i2: 101111
i3: 1111111
c: 1111111111111111
b: 1111111
s: 111111111111111
*///:~
```
A trailing character after a literal value establishes its type. Uppercase or lowercase L means long (however, using a lowercase l is confusing because it can look like the number one). Uppercase or lowercase F means float. Uppercase or lowercase D means double. Hexadecimal (base 16), which works with all the integral data types, is denoted by a leading 0x or 0X followed by 0-9 or a-f either in uppercase or lowercase. If you try to initialize a variable with a value bigger than it can hold (regardless of the numerical form of the value), the compiler will give you an error message. Notice in the preceding code the maximum possible hexadecimal values for char, byte, and short. If you exceed these, the compiler will automatically make the value an int and tell you that you need a narrowing cast for the assignment (casts are defined later in this chapter). You’ll know you’ve stepped over the line. Octal (base 8) is denoted by a leading zero in the number and digits from 0-7. There is no literal representation for binary numbers in C, C++, or Java. However, when working with hexadecimal and octal notation, it’s useful to display the binary form of the results. This is easily accomplished with the static toBinaryString( ) methods from the Integer and Long classes. Notice that when passing smaller types to Integer.toBinaryString( ), the type is automatically converted to an int. Exercise 8: (2) Show that hex and octal notations work with long values. Use Long.toBinaryString( ) to display the results. Exponential notation Exponents use a notation that I’ve always found rather dismaying:

<!--p97-->
```java
//: operators/Exponents.java
// "e" means "10 to the power."
public class Exponents {
public static void main(String[] args) {
// Uppercase and lowercase ‘e’ are the same:
float expFloat = 1.39e-43f;
expFloat = 1.39E-43f;
```
Operators
```java
System.out.println(expFloat);
double expDouble = 47e47d; // ‘d’ is optional
double expDouble2 = 47e47; // Automatically double
System.out.println(expDouble);
}
} /* Output:
1.39E-43
4.7E48
*///:~
```
In science and engineering, ‘e’ refers to the base of natural logarithms, approximately 2.718. (A more precise double value is available in Java as Math.E.) This is used in exponentiation expressions such as 1.39 x e-43, which means 1.39 x 2.718-43. However, when the FORTRAN programming language was invented, they decided that e would mean “ten to the power”, which is an odd decision because FORTRAN was designed for science and engineering, and one would think its designers would be sensitive about introducing such an ambiguity.2At any rate, this custom was followed in C, C++ and now Java. So if you’re used to thinking in terms of e as the base of natural logarithms, you must do a mental translation when you see an expression such as 1.39 e-43f in Java; it means 1.39 x 10-43. Note that you don’t need to use the trailing character when the compiler can figure out the appropriate type. With
```java
long n3 = 200;
```
there’s no ambiguity, so an L after the 200 would be superfluous. However, with
```java
float f4 = 1e-43f; // 10 to the power
```

<!--p98-->

<!--p99-->
the compiler normally takes exponential numbers as doubles, so without the trailing f, it will give you an error telling you that you must use a cast to convert double to float. Exercise 9: (1) Display the largest and smallest numbers for both float and double exponential notation. Bitwise operators The bitwise operators allow you to manipulate individual bits in an integral primitive data type. Bitwise operators perform Boolean algebra on the corresponding bits in the two arguments to produce the result. The bitwise operators come from C’s low-level orientation, where you often manipulate hardware directly and must set the bits in hardware registers. Java was originally designed to be embedded in TV set-top boxes, so this low-level orientation still made sense. However, you probably won’t use the bitwise operators much. 2John Kirkham writes, “I started computing in 1962 using FORTRAN II on an IBM 1620. At that time, and throughout the 1960s and into the 1970s, FORTRAN was an all uppercase language. This probably started because many of the early input devices were old teletype units that used 5 bit Baudot code, which had no lowercase capability. The ‘E’ in the exponential notation was also always uppercase and was never confused with the natural logarithm base ‘e’, which is always lowercase. The ‘E’ simply stood for exponential, which was for the base of the number system used—usually 10. At the time octal was also widely used by programmers. Although I never saw it used, if I had seen an octal number in exponential notation I would have considered it to be base 8. The first time I remember seeing an exponential using a lowercase ‘e’ was in the late 1970s and I also found it confusing. The problem arose as lowercase crept into FORTRAN, not at its beginning. We actually had functions to use if you really wanted to use the natural logarithm base, but they were all uppercase.” The bitwise AND operator (&) produces a one in the output bit if both input bits are one; otherwise, it produces a zero. The bitwise OR operator (|) produces a one in the output bit if either input bit is a one and produces a zero only if both input bits are zero. The bitwise EXCLUSIVE OR, or XOR (^), produces a one in the output bit if one or the other input bit is a one, but not both. The bitwise NOT (~, also called the ones complement operator) is a unary operator; it takes only one argument. (All other bitwise operators are binary operators.) Bitwise NOT produces the opposite of the input bit—a one if the input bit is zero, a zero if the input bit is one. The bitwise operators and logical operators use the same characters, so it is helpful to have a mnemonic device to help you remember the meanings: Because bits are “small”, there is only one character in the bitwise operators. Bitwise operators can be combined with the = sign to unite the operation and assignment: &=, |= and ^= are all legitimate. (Since ~ is a unary operator, it cannot be combined with the = sign.) The boolean type is treated as a one-bit value, so it is somewhat different. You can perform a bitwise AND, OR, and XOR, but you can’t perform a bitwise NOT (presumably to prevent confusion with the logical NOT). For booleans, the bitwise operators have the same effect as the logical operators except that they do not short circuit. Also, bitwise operations on booleans include an XOR logical operator that is not included under the list of “logical” operators. You cannot use booleans in shift expressions, which are described next. Exercise 10: (3) Write a program with two constant values, one with alternating binary ones and zeroes, with a zero in the least-significant digit, and the second, also alternating, with a one in the least-significant digit (hint: It’s easiest to use hexadecimal constants for this). Take these two values and combine them in all possible ways using the bitwise operators, and display the results using Integer.toBinaryString( ). Shift operators The shift operators also manipulate bits. They can be used solely with primitive, integral types. The left-shift operator (<<) produces the operand to the left of the operator after it has been shifted to the left by the number of bits specified to the right of the operator (inserting zeroes at the lower-order bits). The signed right-shift operator (>>) produces the operand to the left of the operator after it has been shifted to the right by the number of bits specified to the right of the operator. The signed right shift >> uses sign extension: If the value is positive, zeroes are inserted at the higher-order bits; if the value is negative, ones are inserted at the higher-order bits. Java has also added the unsigned right shift >>>, which uses zero extension: Regardless of the sign, zeroes are inserted at the higher-order bits. This operator does not exist in C or C++. If you shift a char, byte, or short, it will be promoted to int before the shift takes place, and the result will be an int. Only the five low-order bits of the right-hand side will be used. This prevents you from shifting more than the number of bits in an int. If you’re operating on a long, you’ll get a long result. Only the six low-order bits of the right-hand side will be used, so you can’t shift more than the number of bits in a long. Shifts can be combined with the equal sign (<<= or >>= or >>>=). The lvalue is replaced by the lvalue shifted by the rvalue. There is a problem, however, with the unsigned right shift combined with assignment. If you use it with byte or short, you don’t get the correct results. Instead, these are promoted to int and right shifted, but then truncated as they are assigned back into their variables, so you get -1 in those cases. The following example demonstrates this:
```java
//: operators/URShift.java
// Test of unsigned right shift.
import static net.mindview.util.Print.*;
public class URShift {
public static void main(String[] args) {
int i = -1;
print(Integer.toBinaryString(i));
i >>>= 10;
print(Integer.toBinaryString(i));
long l = -1;
print(Long.toBinaryString(l));
l >>>= 10;
print(Long.toBinaryString(l));
short s = -1;
print(Integer.toBinaryString(s));
s >>>= 10;
print(Integer.toBinaryString(s));
byte b = -1;
print(Integer.toBinaryString(b));
b >>>= 10;
print(Integer.toBinaryString(b));
b = -1;
print(Integer.toBinaryString(b));
print(Integer.toBinaryString(b>>>10));
}
} /* Output:
11111111111111111111111111111111
1111111111111111111111
1111111111111111111111111111111111111111111111111111111111111111
111111111111111111111111111111111111111111111111111111
11111111111111111111111111111111
11111111111111111111111111111111
11111111111111111111111111111111
11111111111111111111111111111111
11111111111111111111111111111111
1111111111111111111111
*///:~
```
In the last shift, the resulting value is not assigned back into b, but is printed directly, so the correct behavior occurs. Here’s an example that demonstrates the use of all the operators involving bits:
```java
//: operators/BitManipulation.java
// Using the bitwise operators.
import java.util.*;
import static net.mindview.util.Print.*;
public class BitManipulation {
public static void main(String[] args) {
Random rand = new Random(47);
int i = rand.nextInt();
int j = rand.nextInt();
printBinaryInt("-1", -1);
printBinaryInt("+1", +1);
int maxpos = 2147483647;
printBinaryInt("maxpos", maxpos);
int maxneg = -2147483648;
printBinaryInt("maxneg", maxneg);
printBinaryInt("i", i);
printBinaryInt("~i", ~i);
```

<!--p100-->
Operators

<!--p101-->
```java
printBinaryInt("-i", -i);
printBinaryInt("j", j);
printBinaryInt("i & j", i & j);
printBinaryInt("i | j", i | j);
printBinaryInt("i ^ j", i ^ j);
printBinaryInt("i << 5", i << 5);
printBinaryInt("i >> 5", i >> 5);
printBinaryInt("(~i) >> 5", (~i) >> 5);
printBinaryInt("i >>> 5", i >>> 5);
printBinaryInt("(~i) >>> 5", (~i) >>> 5);
long l = rand.nextLong();
long m = rand.nextLong();
printBinaryLong("-1L", -1L);
printBinaryLong("+1L", +1L);
long ll = 9223372036854775807L;
printBinaryLong("maxpos", ll);
long lln = -9223372036854775808L;
printBinaryLong("maxneg", lln);
printBinaryLong("l", l);
printBinaryLong("~l", ~l);
printBinaryLong("-l", -l);
printBinaryLong("m", m);
printBinaryLong("l & m", l & m);
printBinaryLong("l | m", l | m);
printBinaryLong("l ^ m", l ^ m);
printBinaryLong("l << 5", l << 5);
printBinaryLong("l >> 5", l >> 5);
printBinaryLong("(~l) >> 5", (~l) >> 5);
printBinaryLong("l >>> 5", l >>> 5);
printBinaryLong("(~l) >>> 5", (~l) >>> 5);
}
static void printBinaryInt(String s, int i) {
print(s + ", int: " + i + ", binary:\n " +
Integer.toBinaryString(i));
}
static void printBinaryLong(String s, long l) {
print(s + ", long: " + l + ", binary:\n " +
Long.toBinaryString(l));
}
} /* Output:
-1, int: -1, binary:
11111111111111111111111111111111
+1, int: 1, binary:
maxpos, int: 2147483647, binary:
1111111111111111111111111111111
maxneg, int: -2147483648, binary:
10000000000000000000000000000000
i, int: -1172028779, binary:
10111010001001000100001010010101
~i, int: 1172028778, binary:
1000101110110111011110101101010
-i, int: 1172028779, binary:
1000101110110111011110101101011
j, int: 1717241110, binary:
1100110010110110000010100010110
i & j, int: 570425364, binary:
100010000000000000000000010100
i | j, int: -25213033, binary:
11111110011111110100011110010111
i ^ j, int: -595638397, binary:
11011100011111110100011110000011
i << 5, int: 1149784736, binary:
1000100100010000101001010100000
i >> 5, int: -36625900, binary:
11111101110100010010001000010100
(~i) >> 5, int: 36625899, binary:
10001011101101110111101011
i >>> 5, int: 97591828, binary:
101110100010010001000010100
(~i) >>> 5, int: 36625899, binary:
10001011101101110111101011
...
*///:~
```
The two methods at the end, printBinaryInt( ) and printBinaryLong( ), take an int or a long, respectively, and print it out in binary format along with a descriptive string. As well as demonstrating the effect of all the bitwise operators for int and long, this example also shows the minimum, maximum, +1, and -1 values for int and long so you can see what they look like. Note that the high bit represents the sign: 0 means positive and 1 means negative. The output for the int portion is displayed above. The binary representation of the numbers is referred to as signed twos complement. Exercise 11: (3) Start with a number that has a binary one in the most significant position (hint: Use a hexadecimal constant). Using the signed right-shift operator, right shift it all the way through all of its binary positions, each time displaying the result using Integer.toBinaryString( ). Exercise 12: (3) Start with a number that is all binary ones. Left shift it, then use the unsigned right-shift operator to right shift through all of its binary positions, each time displaying the result using Integer.toBinaryString( ). Exercise 13: (1) Write a method that displays char values in binary form. Demonstrate it using several different characters.
## Ternary if-else operator
The ternary operator, also called the conditional operator, is unusual because it has three operands. It is truly an operator because it produces a value, unlike the ordinary if-else statement that you’ll see in the next section of this chapter. The expression is of the form:
```java
boolean-exp ? value0 : value1
```
If boolean-exp evaluates to true, value0 is evaluated, and its result becomes the value produced by the operator. If boolean-exp is false, value1 is evaluated and its result becomes the value produced by the operator. Of course, you could use an ordinary if-else statement (described later), but the ternary operator is much terser. Although C (where this operator originated) prides itself on being a terse language, and the ternary operator might have been introduced partly for efficiency, you should be somewhat wary of using it on an everyday basis—it’s easy to produce unreadable code. The conditional operator is different from if-else because it produces a value. Here’s an example comparing the two:
```java
//: operators/TernaryIfElse.java
```

<!--p102-->
Operators
```java
import static net.mindview.util.Print.*;
public class TernaryIfElse {
static int ternary(int i) {
return i < 10 ? i * 100 : i * 10;
}
static int standardIfElse(int i) {
if(i < 10)
return i * 100;
else
return i * 10;
}
public static void main(String[] args) {
print(ternary(9));
print(ternary(10));
print(standardIfElse(9));
print(standardIfElse(10));
}
} /* Output:
*///:~
```
You can see that this code in ternary( ) is more compact than what you’d need to write without the ternary operator, in standardIfElse( ). However, standardIfElse( ) is easier to understand, and doesn’t require a lot more typing. So be sure to ponder your reasons when choosing the ternary operator—it’s generally warranted when you’re setting a variable to one of two values.
## String operator + and +=
There’s one special usage of an operator in Java: The + and += operators can be used to concatenate strings, as you’ve already seen. It seems a natural use of these operators even though it doesn’t fit with the traditional way that they are used. This capability seemed like a good idea in C++, so operator overloading was added to C++ to allow the C++ programmer to add meanings to almost any operator. Unfortunately, operator overloading combined with some of the other restrictions in C++ turns out to be a fairly complicated feature for programmers to design into their classes. Although operator overloading would have been much simpler to implement in Java than it was in C++ (as has been demonstrated in the C# language, which does have straightforward operator overloading), this feature was still considered too complex, so Java programmers cannot implement their own overloaded operators like C++ and C# programmers can. The use of the String operators has some interesting behavior. If an expression begins with a String, then all operands that follow must be Strings (remember that the compiler automatically turns a double-quoted sequence of characters into a String):

<!--p103-->
```java
//: operators/StringOperators.java
import static net.mindview.util.Print.*;
public class StringOperators {
public static void main(String[] args) {
int x = 0, y = 1, z = 2;
String s = "x, y, z ";
print(s + x + y + z);
print(x + " " + s); // Converts x to a String
s += "(summed) = "; // Concatenation operator
print(s + (x + y + z));
print("" + x); // Shorthand for Integer.toString()
}
} /* Output:
x, y, z 012
0 x, y, z
x, y, z (summed) = 3
*///:~
```
Note that the output from the first print statement is ‘o12’ instead of just ‘3’, which is what you’d get if it was summing the integers. This is because the Java compiler converts x, y, and z into their String representations and concatenates those strings, instead of adding them together first. The second print statement converts the leading variable into a String, so the string conversion does not depend on what comes first. Finally, you see the use of the += operator to append a string to s, and the use of parentheses to control the order of evaluation of the expression so that the ints are actually summed before they are displayed. Notice the last example in main( ): you will sometimes see an empty String followed by a + and a primitive as a way to perform the conversion without calling the more cumbersome explicit method (Integer.toString( ), in this case). Common pitfalls when using operators One of the pitfalls when using operators is attempting to leave out the parentheses when you are even the least bit uncertain about how an expression will evaluate. This is still true in Java. An extremely common error in C and C++ looks like this:
```java
while(x = y) {
// ....
}
```

<!--p104-->
The programmer was clearly trying to test for equivalence (==) rather than do an assignment. In C and C++ the result of this assignment will always be true if y is nonzero, and you’ll probably get an infinite loop. In Java, the result of this expression is not a boolean, but the compiler expects a boolean and won’t convert from an int, so it will conveniently give you a compile-time error and catch the problem before you ever try to run the program. So the pitfall never happens in Java. (The only time you won’t get a compile- time error is when x and y are boolean, in which case x = y is a legal expression, and in the preceding example, probably an error.) A similar problem in C and C++ is using bitwise AND and OR instead of the logical versions. Bitwise AND and OR use one of the characters (& or |) while logical AND and OR use two (&& and ||). Just as with = and ==, it’s easy to type just one character instead of two. In Java, the compiler again prevents this, because it won’t let you cavalierly use one type where it doesn’t belong. Casting operators The word cast is used in the sense of “casting into a mold.” Java will automatically change one type of data into another when appropriate. For instance, if you assign an integral value to a floating point variable, the compiler will automatically convert the int to a float. Casting Operators allows you to make this type conversion explicit, or to force it when it wouldn’t normally happen. To perform a cast, put the desired data type inside parentheses to the left of any value. You can see this in the following example:
```java
//: operators/Casting.java
public class Casting {
public static void main(String[] args) {
int i = 200;
long lng = (long)i;
lng = i; // "Widening," so cast not really required
long lng2 = (long)200;
lng2 = 200;
// A "narrowing conversion":
i = (int)lng2; // Cast required
}
} ///:~
```
As you can see, it’s possible to perform a cast on a numeric value as well as on a variable. Notice that you can introduce superfluous casts; for example, the compiler will automatically promote an int value to a long when necessary. However, you are allowed to use superfluous casts to make a point or to clarify your code. In other situations, a cast may be essential just to get the code to compile. In C and C++, casting can cause some headaches. In Java, casting is safe, with the exception that when you perform a so-called narrowing conversion (that is, when you go from a data type that can hold more information to one that doesn’t hold as much), you run the risk of losing information. Here the compiler forces you to use a cast, in effect saying, “This can be a dangerous thing to do—if you want me to do it anyway you must make the cast explicit.” With a widening conversion an explicit cast is not needed, because the new type will more than hold the information from the old type so that no information is ever lost. Java allows you to cast any primitive type to any other primitive type, except for boolean, which doesn’t allow any casting at all. Class types do not allow casting. To convert one to the other, there must be special methods. (You’ll find out later in this book that objects can be cast within a family of types; an Oak can be cast to a Tree and vice versa, but not to a foreign type such as a Rock.) Truncation and rounding When you are performing narrowing conversions, you must pay attention to issues of truncation and rounding. For example, if you cast from a floating point value to an integral value, what does Java do? For example, if you have the value 29.7 and you cast it to an int, is the resulting value 30 or 29? The answer to this can be seen in this example:

<!--p105-->
```java
//: operators/CastingNumbers.java
// What happens when you cast a float
// or double to an integral value?
import static net.mindview.util.Print.*;
public class CastingNumbers {
public static void main(String[] args) {
double above = 0.7, below = 0.4;
float fabove = 0.7f, fbelow = 0.4f;
print("(int)above: " + (int)above);
print("(int)below: " + (int)below);
print("(int)fabove: " + (int)fabove);
print("(int)fbelow: " + (int)fbelow);
}
} /* Output:
(int)above: 0
(int)below: 0
(int)fabove: 0
(int)fbelow: 0
*///:~
```
So the answer is that casting from a float or double to an integral value always truncates the number. If instead you want the result to be rounded, use the round( ) methods in java.lang.Math:
```java
//: operators/RoundingNumbers.java
// Rounding floats and doubles.
import static net.mindview.util.Print.*;
public class RoundingNumbers {
public static void main(String[] args) {
double above = 0.7, below = 0.4;
float fabove = 0.7f, fbelow = 0.4f;
print("Math.round(above): " + Math.round(above));
print("Math.round(below): " + Math.round(below));
print("Math.round(fabove): " + Math.round(fabove));
print("Math.round(fbelow): " + Math.round(fbelow));
}
} /* Output:
Math.round(above): 1
Math.round(below): 0
Math.round(fabove): 1
Math.round(fbelow): 0
*///:~
```

<!--p106-->
Since the round( ) is part of java.lang, you don’t need an extra import to use it. Promotion You’ll discover that if you perform any mathematical or bitwise operations on primitive data types that are smaller than an int (that is, char, byte, or short), those values will be promoted to int before performing the operations, and the resulting value will be of type int. So if you want to assign back into the smaller type, you must use a cast. (And, since you’re assigning back into a smaller type, you might be losing information.) In general, the largest data type in an expression is the one that determines the size of the result of that expression; if you multiply a float and a double, the result will be double; if you add an int and a long, the result will be long. Java has no “sizeof” In C and C++, the sizeof( ) operator tells you the number of bytes allocated for data items. The most compelling reason for sizeof( ) in C and C++ is for portability. Different data types might be different sizes on different machines, so the programmer must discover how big those types are when performing operations that are sensitive to size. For example, one computer might store integers in 32 bits, whereas another might store integers as 16 bits. Programs could store larger values in integers on the first machine. As you might imagine, portability is a huge headache for C and C++ programmers. Operators Java does not need a sizeof( ) operator for this purpose, because all the data types are the same size on all machines. You do not need to think about portability on this level—it is designed into the language. A compendium of operators The following example shows which primitive data types can be used with particular operators. Basically, it is the same example repeated over and over, but using different primitive data types. The file will compile without error because the lines that fail are commented out with a //!.

<!--p107-->
```java
//: operators/AllOps.java
// Tests all the operators on all the primitive data types
// to show which ones are accepted by the Java compiler.
public class AllOps {
// To accept the results of a boolean test:
void f(boolean b) {}
void boolTest(boolean x, boolean y) {
// Arithmetic operators:
//! x = x * y;
//! x = x / y;
//! x = x % y;
//! x = x + y;
//! x = x - y;
//! x++;
//! x--;
//! x = +y;
//! x = -y;
// Relational and logical:
//! f(x > y);
//! f(x >= y);
//! f(x < y);
//! f(x <= y);
f(x == y);
f(x != y);
f(!y);
x = x && y;
x = x || y;
// Bitwise operators:
//! x = ~y;
x = x & y;
x = x | y;
x = x ^ y;
//! x = x << 1;
//! x = x >> 1;
//! x = x >>> 1;
// Compound assignment:
//! x += y;
//! x -= y;
//! x *= y;
//! x /= y;
//! x %= y;
//! x <<= 1;
//! x >>= 1;
//! x >>>= 1;
x &= y;
x ^= y;
x |= y;
// Casting:
//! char c = (char)x;
//! byte b = (byte)x;
//! short s = (short)x;
//! int i = (int)x;
//! long l = (long)x;
//! float f = (float)x;
//! double d = (double)x;
}
void charTest(char x, char y) {
// Arithmetic operators:
x = (char)(x * y);
x = (char)(x / y);
x = (char)(x % y);
x = (char)(x + y);
x = (char)(x - y);
x++;
x--;
x = (char)+y;
x = (char)-y;
// Relational and logical:
f(x > y);
f(x >= y);
f(x < y);
f(x <= y);
f(x == y);
f(x != y);
//! f(!x);
//! f(x && y);
//! f(x || y);
// Bitwise operators:
x= (char)~y;
x = (char)(x & y);
x = (char)(x | y);
x = (char)(x ^ y);
x = (char)(x << 1);
x = (char)(x >> 1);
x = (char)(x >>> 1);
// Compound assignment:
x += y;
x -= y;
x *= y;
x /= y;
x %= y;
x <<= 1;
x >>= 1;
x >>>= 1;
x &= y;
x ^= y;
x |= y;
// Casting:
//! boolean bl = (boolean)x;
byte b = (byte)x;
short s = (short)x;
int i = (int)x;
long l = (long)x;
float f = (float)x;
double d = (double)x;
}
void byteTest(byte x, byte y) {
// Arithmetic operators:
x = (byte)(x* y);
x = (byte)(x / y);
x = (byte)(x % y);
```

<!--p108-->
Operators

<!--p109-->
```java
x = (byte)(x + y);
x = (byte)(x - y);
x++;
x--;
x = (byte)+ y;
x = (byte)- y;
// Relational and logical:
f(x > y);
f(x >= y);
f(x < y);
f(x <= y);
f(x == y);
f(x != y);
//! f(!x);
//! f(x && y);
//! f(x || y);
// Bitwise operators:
x = (byte)~y;
x = (byte)(x & y);
x = (byte)(x | y);
x = (byte)(x ^ y);
x = (byte)(x << 1);
x = (byte)(x >> 1);
x = (byte)(x >>> 1);
// Compound assignment:
x += y;
x -= y;
x *= y;
x /= y;
x %= y;
x <<= 1;
x >>= 1;
x >>>= 1;
x &= y;
x ^= y;
x |= y;
// Casting:
//! boolean bl = (boolean)x;
char c = (char)x;
short s = (short)x;
int i = (int)x;
long l = (long)x;
float f = (float)x;
double d = (double)x;
}
void shortTest(short x, short y) {
// Arithmetic operators:
x = (short)(x * y);
x = (short)(x / y);
x = (short)(x % y);
x = (short)(x + y);
x = (short)(x - y);
x++;
x--;
x = (short)+y;
x = (short)-y;
// Relational and logical:
f(x > y);
f(x >= y);
f(x < y);
f(x <= y);
f(x == y);
f(x != y);
//! f(!x);
//! f(x && y);
//! f(x || y);
// Bitwise operators:
x = (short)~y;
x = (short)(x & y);
x = (short)(x | y);
x = (short)(x ^ y);
x = (short)(x << 1);
x = (short)(x >> 1);
x = (short)(x >>> 1);
// Compound assignment:
x += y;
x -= y;
x *= y;
x /= y;
x %= y;
x <<= 1;
x >>= 1;
x >>>= 1;
x &= y;
x ^= y;
x |= y;
// Casting:
//! boolean bl = (boolean)x;
char c = (char)x;
byte b = (byte)x;
int i = (int)x;
long l = (long)x;
float f = (float)x;
double d = (double)x;
}
void intTest(int x, int y) {
// Arithmetic operators:
x = x * y;
x = x / y;
x = x % y;
x = x + y;
x = x - y;
x++;
x--;
x = +y;
x = -y;
// Relational and logical:
f(x > y);
f(x >= y);
f(x < y);
f(x <= y);
f(x == y);
f(x != y);
//! f(!x);
//! f(x && y);
//! f(x || y);
// Bitwise operators:
x = ~y;
x = x & y;
x = x | y;
x = x ^ y;
x = x << 1;
x = x >> 1;
x = x >>> 1;
// Compound assignment:
x += y;
```

<!--p110-->
Operators

<!--p111-->
```java
x -= y;
x *= y;
x /= y;
x %= y;
x <<= 1;
x >>= 1;
x >>>= 1;
x &= y;
x ^= y;
x |= y;
// Casting:
//! boolean bl = (boolean)x;
char c = (char)x;
byte b = (byte)x;
short s = (short)x;
long l = (long)x;
float f = (float)x;
double d = (double)x;
}
void longTest(long x, long y) {
// Arithmetic operators:
x = x * y;
x = x / y;
x = x % y;
x = x + y;
x = x - y;
x++;
x--;
x = +y;
x = -y;
// Relational and logical:
f(x > y);
f(x >= y);
f(x < y);
f(x <= y);
f(x == y);
f(x != y);
//! f(!x);
//! f(x && y);
//! f(x || y);
// Bitwise operators:
x = ~y;
x = x & y;
x = x | y;
x = x ^ y;
x = x << 1;
x = x >> 1;
x = x >>> 1;
// Compound assignment:
x += y;
x -= y;
x *= y;
x /= y;
x %= y;
x <<= 1;
x >>= 1;
x >>>= 1;
x &= y;
x ^= y;
x |= y;
// Casting:
//! boolean bl = (boolean)x;
char c = (char)x;
byte b = (byte)x;
short s = (short)x;
int i = (int)x;
float f = (float)x;
double d = (double)x;
}
void floatTest(float x, float y) {
// Arithmetic operators:
x = x * y;
x = x / y;
x = x % y;
x = x + y;
x = x - y;
x++;
x--;
x = +y;
x = -y;
// Relational and logical:
f(x > y);
f(x >= y);
f(x < y);
f(x <= y);
f(x == y);
f(x != y);
//! f(!x);
//! f(x && y);
//! f(x || y);
// Bitwise operators:
//! x = ~y;
//! x = x & y;
//! x = x | y;
//! x = x ^ y;
//! x = x << 1;
//! x = x >> 1;
//! x = x >>> 1;
// Compound assignment:
x += y;
x -= y;
x *= y;
x /= y;
x %= y;
//! x <<= 1;
//! x >>= 1;
//! x >>>= 1;
//! x &= y;
//! x ^= y;
//! x |= y;
// Casting:
//! boolean bl = (boolean)x;
char c = (char)x;
byte b = (byte)x;
short s = (short)x;
int i = (int)x;
long l = (long)x;
double d = (double)x;
}
void doubleTest(double x, double y) {
// Arithmetic operators:
x = x * y;
x = x / y;
x = x % y;
x = x + y;
x = x - y;
```

<!--p112-->
Operators
```java
x++;
x--;
x = +y;
x = -y;
// Relational and logical:
f(x > y);
f(x >= y);
f(x < y);
f(x <= y);
f(x == y);
f(x != y);
//! f(!x);
//! f(x && y);
//! f(x || y);
// Bitwise operators:
//! x = ~y;
//! x = x & y;
//! x = x | y;
//! x = x ^ y;
//! x = x << 1;
//! x = x >> 1;
//! x = x >>> 1;
// Compound assignment:
x += y;
x -= y;
x *= y;
x /= y;
x %= y;
//! x <<= 1;
//! x >>= 1;
//! x >>>= 1;
//! x &= y;
//! x ^= y;
//! x |= y;
// Casting:
//! boolean bl = (boolean)x;
char c = (char)x;
byte b = (byte)x;
short s = (short)x;
int i = (int)x;
long l = (long)x;
float f = (float)x;
}
} ///:~
```
Note that boolean is quite limited. You can assign to it the values true and false, and you can test it for truth or falsehood, but you cannot add booleans or perform any other type of operation on them. In char, byte, and short, you can see the effect of promotion with the arithmetic operators. Each arithmetic operation on any of those types produces an int result, which must be explicitly cast back to the original type (a narrowing conversion that might lose information) to assign back to that type. With int values, however, you do not need to cast, because everything is already an int. Don’t be lulled into thinking everything is safe, though. If you multiply two ints that are big enough, you’ll overflow the result. The following example demonstrates this:

<!--p113-->
```java
//: operators/Overflow.java
// Surprise! Java lets you overflow.
public class Overflow {
public static void main(String[] args) {
```
Operators
```java
int big = Integer.MAX_VALUE;
System.out.println("big = " + big);
int bigger = big * 4;
System.out.println("bigger = " + bigger);
}
} /* Output:
big = 2147483647
bigger = -4
*///:~
```
You get no errors or warnings from the compiler, and no exceptions at run time. Java is good, but it’s not that good. Compound assignments do not require casts for char, byte, or short, even though they are performing promotions that have the same results as the direct arithmetic operations. On the other hand, the lack of the cast certainly simplifies the code. You can see that, with the exception of boolean, any primitive type can be cast to any other primitive type. Again, you must be aware of the effect of a narrowing conversion when casting to a smaller type; otherwise, you might unknowingly lose information during the cast. Exercise 14: (3) Write a method that takes two String arguments and uses all the boolean comparisons to compare the two Strings and print the results. For the == and !=, also perform the equals( ) test. In main( ), call your method with some different String objects. Summary If you’ve had experience with any languages that use C-like syntax, you can see that the operators in Java are so similar that there is virtually no learning curve. If you found this chapter challenging, make sure you view the multimedia presentation Thinking in C, available at www.MindView.net. Solutions to selected exercises can be found in the electronic document The Thinking in Java Annotated Solution Guide, available for sale from www.MindView.net.