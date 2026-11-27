# 13. Strings (printed p355-392)


<!--p377-->
Strings String manipulation is arguably one of the most common activities in computer programming. This is especially true in Web systems, where Java is heavily used. In this chapter, we’ll look more deeply at what is certainly the most commonly used class in the language, String, along with some of its associated classes and utilities.
## Immutable Strings
Objects of the String class are immutable. If you examine the JDK documentation for the String class, you’ll see that every method in the class that appears to modify a String actually creates and returns a brand new String object containing the modification. The original String is left untouched. Consider the following code:
```java
//: strings/Immutable.java
import static net.mindview.util.Print.*;
public class Immutable {
public static String upcase(String s) {
return s.toUpperCase();
}
public static void main(String[] args) {
String q = "howdy";
print(q); // howdy
String qq = upcase(q);
print(qq); // HOWDY
print(q); // howdy
}
} /* Output:
howdy
HOWDY
howdy
*///:~
```
When q is passed in to upcase( ) it’s actually a copy of the reference to q. The object this reference is connected to stays in a single physical location. The references are copied as they are passed around. Looking at the definition for upcase( ), you can see that the reference that’s passed in has the name s, and it exists for only as long as the body of upcase( ) is being executed. When upcase( ) completes, the local reference s vanishes. upcase( ) returns the result, which is the original string with all the characters set to uppercase. Of course, it actually returns a reference to the result. But it turns out that the reference that it returns is for a new object, and the original q is left alone. This behavior is usually what you want. Suppose you say:

<!--p378-->
```java
String s = "asdf";
String x = Immutable.upcase(s);
```
Do you really want the upcase( ) method to change the argument? To the reader of the code, an argument usually looks like a piece of information provided to the method, not something to be modified. This is an important guarantee, since it makes code easier to write and understand.
## Overloading ‘+’ vs. StringBuilder
Since String objects are immutable, you can alias to a particular String as many times as you want. Because a String is read-only, there’s no possibility that one reference will change something that will affect the other references. Immutability can have efficiency issues. A case in point is the operator ‘+’ that has been overloaded for String objects. Overloading means that an operation has been given an extra meaning when used with a particular class. (The ‘+’ and ‘+=‘ for String are the only operators that are overloaded in Java, and Java does not allow the programmer to overload any others.)1 The’+’ operator allows you to concatenate Strings:
```java
//: strings/Concatenation.java
public class Concatenation {
public static void main(String[] args) {
String mango = "mango";
String s = "abc" + mango + "def" + 47;
System.out.println(s);
}
} /* Output:
abcmangodef47
*///:~
```
You could imagine how this might work. The String "abc" could have a method append( ) that creates a new String object containing "abc" concatenated with the contents of mango. The new String object would then create another new String that added "def," and so on. This would certainly work, but it requires the creation of a lot of String objects just to put together this new String, and then you have a bunch of intermediate String objects that need to be garbage collected. I suspect that the Java designers tried this approach first (which is a lesson in software design—you don’t really know anything about a system until you try it out in code and get something working). I also suspect that they discovered it delivered unacceptable performance. To see what really happens, you can decompile the above code using the javap tool that comes as part of the JDK. Here’s the command line:
```java
javap -c Concatenation
```
The -c flag will produce the JVM bytecodes. After we strip out the parts we’re not interested in and do a bit of editing, here are the relevant bytecodes:
```java
public static void main(java.lang.String[]);
Code:
Stack=2, Locals=3, Args_size=1
0: ldc #2; //String mango
```

<!--p379-->
1C++ allows the programmer to overload operators at will. Because this can often be a complicated process (see Chapter 10 of Thinking in C++, 2nd Edition, Prentice Hall, 2000), the Java designers deemed it a "bad" feature that shouldn’t be included in Java. It wasn’t so bad that they didn’t end up doing it themselves, and ironically enough, operator overloading would be much easier to use in Java than in C++. This can be seen in Python (see www.Python.org) and C#, which have garbage collection and straightforward operator overloading.
```java
2: astore_1
3: new #3; //class StringBuilder
6: dup
7: invokespecial #4; //StringBuilder."<init>":()
10: ldc #5; // String abc
12 invokevirtual #6; //StringBuilder.append:(String)
15 aload_1
16 invokevirtual #6; //StringBuilder.append:(String)
19 ldc #7; //String def
21 invokevirtual #6; //StringBuilder.append:(String)
24 bipush 47
26 invokevirtual #8; //StringBuilder.append:(I)
29 invokevirtual #9; //StringBuilder.toString:()
32 astore_2
33 getstatic #10; //Field System.out:PrintStream;
36 aload_2
37 invokevirtual #11; // PrintStream.println:(String)
40 return
```
If you’ve had experience with assembly language, this may look familiar to you—statements like dup and invokevirtual are the Java Virtual Machine (JVM) equivalent of assembly language. If you’ve never seen assembly language, don’t worry about it—the important part to notice is the introduction by the compiler of the java.lang.StringBuilder class. There was no mention of StringBuilder in the source code, but the compiler decided to use it anyway, because it is much more efficient. In this case, the compiler creates a StringBuilder object to build the String s, and calls append( ) four times, one for each of the pieces. Finally, it calls toString( ) to produce the result, which it stores (with astore_2)as s. Before you assume that you should just use Strings everywhere and that the compiler will make everything efficient, let’s look a little more closely at what the compiler is doing. Here’s an example that produces a String result in two ways: using Strings, and by hand-coding with StringBuilder:
```java
//: strings/WhitherStringBuilder.java
public class WhitherStringBuilder {
public String implicit(String[] fields) {
String result = "";
for(int i = 0; i < fields.length; i++)
result += fields[i];
return result;
}
public String explicit(String[] fields) {
StringBuilder result = new StringBuilder();
for(int i = 0; i < fields.length; i++)
result.append(fields[i]);
return result.toString();
}
} ///:~
```
Now if you run javap -c WitherStringBuilder, you can see the (simplified) code for the two different methods. First, implicit( ):
```java
public java.lang.String implicit(java.lang.String[]);
Code:
0: ldc #2; //String
2: astore_2
3: iconst_0
4: istore_3
```

<!--p380-->
Strings
```java
5: iload_3
6: aload_1
7: arraylength
8: if_icmpge 38
11: new #3; //class StringBuilder
14: dup
15: invokespecial #4; // StringBuilder.”<init>”:()
18: aload_2
19: invokevirtual #5; // StringBuilder.append:()
22: aload_1
23 iload_3
24 aaload
25: invokevirtual #5; // StringBuilder.append:()
28: invokevirtual #6; // StringBuiIder.toString:()
31: astore_2
32: iinc 3, 1
35: goto 5
38: aload_2
39 areturn
```
Notice 8: and 35:, which together form a loop. 8: does an "integer compare greater than or equal to" of the operands on the stack and jumps to 38: when the loop is done. 35: is a goto back to the beginning of the loop, at 5:. The important thing to note is that the StringBuilder construction happens inside this loop, which means you’re going to get a new StringBuilder object every time you pass through the loop. Here are the bytecodes for explicit( ):
```java
public java.lang.String explicit(java.lang.String[]);
Code:
0: new #3; //class StringBuilder
3: dup
4: invokespecial #4; // StringBuilder.”<init>”:()
7: astore_2
8: iconst_0
9: istore_3
10: iload_3
11: aload_1
12: arraylength
13: if_icmpge 30
16: aload_2
17: aload_1
18: iload_3
19: aaload
20 invokevirtual #5; // StringBuilder.append:()
23 pop
24: iinc 3,1
27: goto 10
30: aload_2
31: invokevirtual #6; // StringBuiIder.toString:()
34: areturn
```

<!--p381-->
Not only is the loop code shorter and simpler, the method only creates a single StringBuilder object. Creating an explicit StringBuilder also allows you to preallocate its size if you have extra information about how big it might need to be, so that it doesn’t need to constantly reallocate the buffer. Thus, when you create a toString( ) method, if the operations are simple ones that the compiler can figure out on its own, you can generally rely on the compiler to build the result in a reasonable fashion. But if looping is involved, you should explicitly use a StringBuilder in your toString( ), like this:
```java
//: strings/UsingStringBuilder.java
import java.util.*;
public class UsingStringBuilder {
public static Random rand = new Random(47);
public String toString() {
StringBuilder result = new StringBuilder("[");
for(int i = 0; i < 25; i++) {
result.append(rand.nextInt(100));
result.append(", ");
}
result.delete(result.length()-2, result.length());
result.append("]");
return result.toString();
}
public static void main(String[] args) {
UsingStringBuilder usb = new UsingStringBuilder();
System.out.println(usb);
}
} /* Output:
[58, 55, 93, 61, 61, 29, 68, 0, 22, 7, 88, 28, 51, 89, 9, 78, 98, 61,
20, 58, 16, 40, 11, 22, 4]
*///:~
```
Notice that each piece of the result is added with an append( ) statement. If you try to take shortcuts and do something like append(a + ": " +c), the compiler will jump in and start making more StringBuilder objects again. If you are in doubt about which approach to use, you can always run javap to double-check. Although StringBuilder has a full complement of methods, including insert( ), replace( ), substring( ) and even reverse( ), the ones you will generally use are append( ) and toString( ). Note the use of delete( ) to remove the last comma and space before adding the closing square bracket. StringBuilder was introduced in Java SE5. Prior to this, Java used StringBuffer, which ensured thread safety (see the Concurrency chapter) and so was significantly more expensive. Thus, string operations in Java SE5/6 should be faster. Exercise 1:(2) Analyze SprinklerSystem.toString( ) in reusing/SprinklerSystem.java to discover whether writing the toString( ) with an explicit StringBuilder will save any StringBuilder creations. Unintended recursion Because (like every other class) the Java standard containers are ultimately inherited from Object, they contain a toString( ) method. This has been overridden so that they can produce a String representation of themselves, including the objects they hold. ArrayList.toString( ), for example, steps through the elements of the Array List and calls toString( ) for each one:
```java
//: strings/ArrayListDisplay.java
import generics.coffee.*;
```

<!--p382-->
Strings
```java
import java.util.*;
public class ArrayListDisplay {
public static void main(String[] args) {
ArrayList<Coffee> coffees = new ArrayList<Coffee>();
for(Coffee c : new CoffeeGenerator(10))
coffees.add(c);
System.out.println(coffees);
}
} /* Output:
[Americano 0, Latte 1, Americano 2, Mocha 3, Mocha 4, Breve 5, Americano
6, Latte 7, Cappuccino 8, Cappuccino 9]
*///:~
```
Suppose you’d like your toString( ) to print the address of your class. It seems to make sense to simply refer to this:
```java
//: strings/InfiniteRecursion.java
// Accidental recursion.
// {RunByHand}
import java.util.*;
public class InfiniteRecursion {
public String toString() {
return " InfiniteRecursion address: " + this + "\n";
}
public static void main(String[] args) {
List<InfiniteRecursion> v =
new ArrayList<InfiniteRecursion>();
for(int i = 0; i < 10; i++)
v.add(new InfiniteRecursion());
System.out.println(v);
}
} ///:~
```
If you create an InfiniteRecursion object and then print it, you’ll get a very long sequence of exceptions. This is also true if you place the InfiniteRecursion objects in an ArrayList and print that ArrayList as shown here. What’s happening is automatic type conversion for Strings. When you say:
```java
"InfiniteRecursion address: " + this
```

<!--p383-->
The compiler sees a String followed by a’+’ and something that’s not a String, so it tries to convert this to a String. It does this conversion by calling toString( ), which produces a recursive call. If you really do want to print the address of the object, the solution is to call the ObjecttoString( ) method, which does just that. So instead of saying this, you’d say super.toString( ). Exercise 2:(1) Repair InfiniteRecursion.java.
## Operations on Strings

<!--p384-->

<!--p385-->
Here are some of the basic methods available for String objects. Methods that are overloaded are summarized in a single row: Method Arguments, Overloading Use Constructor Overloaded: default, String, StringBuilder, StringBuffer, char arrays, byte arrays. Creating String objects. length( ) Number of characters in the String. charAt( ) int Index The char at a location in the String. getChars( ), getBytes( ) The beginning and end from which to copy, the array to copy into, an index into the destination array. Copy chars or bytes into an external array. toCharArray( ) Produces a char[] containing the charactersin the String. equals( ), equals- IgnoreCase( ) A String to compare with. An equality check on the contents of the two Strings. compareTo( ) A String to compare with. Result is negative, zero, or positive depending on the lexicographical ordering of the String and the argument. Uppercase and lowercase are not equal! contains( ) A CharSequence to search for. Result is true if the argument is contained in the String. contentEquals( ) A CharSequence or StringBuffer to compare to. Result is true if there’s an exact match with the argument. equalsIgnoreCase( ) A String to compare with. Result is true if the contents are equal, ignoring case. regionMatches( ) Offset into this String, the other String and its offset and length to compare. Overload adds "ignore case." boolean result indicates whether the region matches. startsWith( ) String that it might start with. Overload adds offset into argument. boolean result indicates whether the String starts with the argument. endsWith( ) String that might be a suffix of this String. boolean result indicates whether the argument is a suffix. indexOf( ), lastIndexOf( ) Overloaded: char, char and startingindex, String, Returns -1 if the argument is not found within this String; otherwise, returns Strings Method Arguments, Overloading Use String and startingindex. the index where the argument starts. lastIndexOf( ) searches backward from end. substring( ) (also subSequence( )) Overloaded: starting index; starting index + ending index. Returns a new String object containing thespecified character set. concat( ) The String to concatenate. Returns a new String object containing theoriginal String’scharacters followed bythe characters in the argument. replace() The old character to search for, the new character to replace it with. Can also replace a CharSequence with a CharSequence. Returns a new String object with the replacements made. Uses the old String if no match is found. toLowerCase( ) toUpperCase( ) Returns a new String object with the case of allletters changed. Uses theold String if no changesneed to be made. trim( ) Returns a new String object with thewhitespace removed from each end. Uses theold String if no changesneed to be made. valueOf( ) Overloaded: Object, char[], char[] andoffset and count, boolean, char, int, long, float, double. Returns a String containing a characterrepresentation of theargument. intern( ) Produces one and only one String reference per unique character sequence. You can see that every String method carefully returns a new String object when it’s necessary to change the contents. Also notice that if the contents don’t need changing, the method will just return a reference to the original String. This saves storage and overhead. The String methods involving regular expressions will be explained later in this chapter. Formatting output One of the long-awaited features that has finally appeared in Java SE5 is output formatting in the style of C’s printf( ) statement. Not only does this allow for simplified output code, but it also gives Java developers powerful control over output formatting and alignment.2 2Mark Welsh assisted in the creation of this section, and the "Scanning input" section.
## printf()
C’s printf( ) doesn’t assemble strings the way Java does, but takes a single format string and inserts values into it, formatting as it goes. Instead of using the overloaded ‘+’ operator (which C doesn’t overload) to concatenate quoted text and variables, printf( ) uses special placeholders to show where the data should go. The arguments that are inserted into the format string follow in a comma-separated list. For example:
```java
printf("Row 1: [%d %f]\n", x, y);
```
At run time, the value of x is inserted into %d and the value of y is inserted into %f. These placeholders are called/ormaf specifiers and, in addition to telling where to insert the value, they also tell what kind of variable is to be inserted and how to format it. For instance, the ‘%d’ above says that x is an integer and the ‘%f says y is a floating point value (a float or double).
## System.out.format()
Java SE5 introduced the format( ) method, available to PrintStream or PrintWriter objects (which you’ll learn more about in the I/O chapter), which includes System.out. The format( ) method is modeled after C’s printf( ). There’s even a convenience printf( ) method that you can use if you’re feeling nostalgic, which just calls format( ). Here’s a simple example:
```java
//: strings/SimpleFormat.java
public class SimpleFormat {
public static void main(String[] args) {
int x = 5;
double y = 5.332542;
// The old way:
System.out.println("Row 1: [" + x + " " + y + "]");
// The new way:
System.out.format("Row 1: [%d %f]\n", x, y);
// or
System.out.printf("Row 1: [%d %f]\n", x, y);
}
} /* Output:
Row 1: [5 5.332542]
Row 1: [5 5.332542]
Row 1: [5 5.332542]
*///:~
```
You can see that format( ) and printf( ) are equivalent. In both cases, there’s only a single format string, followed by one argument for each format specifier.
## The Formatter class
All of Java’s new formatting functionality is handled by the Formatter class in the java.util package. You can think of Formatter as a translator that converts your format string and data into the desired result. When you create a Formatter object, you tell it where you want this result to go by passing that information to the constructor:
```java
//: strings/Turtle.java
```

<!--p386-->
Strings
```java
import java.io.*;
import java.util.*;
public class Turtle {
private String name;
private Formatter f;
public Turtle(String name, Formatter f) {
this.name = name;
this.f = f;
}
public void move(int x, int y) {
f.format("%s The Turtle is at (%d,%d)\n", name, x, y);
}
public static void main(String[] args) {
PrintStream outAlias = System.out;
Turtle tommy = new Turtle("Tommy",
new Formatter(System.out));
Turtle terry = new Turtle("Terry",
new Formatter(outAlias));
tommy.move(0,0);
terry.move(4,8);
tommy.move(3,4);
terry.move(2,5);
tommy.move(3,3);
terry.move(3,3);
}
} /* Output:
Tommy The Turtle is at (0,0)
Terry The Turtle is at (4,8)
Tommy The Turtle is at (3,4)
Terry The Turtle is at (2,5)
Tommy The Turtle is at (3,3)
Terry The Turtle is at (3,3)
*///:~
```
All the tommy output goes to System.out and all the terry output goes to an alias of System.out. The constructor is overloaded to take a range of output locations, but the most useful are PrintStreams (as above), OutputStreams, and Files. You’ll learn more about these in the I/O chapter. Exercise 3:(1) Modify Turtle.java so that it sends all output to System.err. The previous example uses a new format specifier, ‘%s’. This indicates a String argument and is an example of the simplest kind of format specifier-one that has only a conversion type. Format specifiers To control spacing and alignment when data is inserted, you need more elaborate format specifiers. Here’s the general syntax:
```java
%[argument_index$][flags][width][.precision]conversion
```

<!--p387-->
Often, you’ll need to control the minimum size of a field. This can be accomplished by specifying a width. The Formatter guarantees that a field is at least a certain number of characters wide by padding it with spaces if necessary. By default, the data is right justified, but this can be overridden by including a ‘-’ in the flags section. The opposite of width is precision, which is used to specify a maximum. Unlike the width, which is applicable to all of the data conversion types and behaves the same with each, precision has a different meaning for different types. For Strings, the precision specifies the maximum number of characters from the String to print. For floating point numbers, precision specifies the number of decimal places to display (the default is 6), rounding if there are too many or adding trailing zeroes if there are too few. Since integers have no fractional part, precision isn’t applicable to them and you’ll get an exception if you use precision with an integer conversion type. This example uses format specifiers to print a shopping receipt:
```java
//: strings/Receipt.java
import java.util.*;
public class Receipt {
private double total = 0;
private Formatter f = new Formatter(System.out);
public void printTitle() {
f.format("%-15s %5s %10s\n", "Item", "Qty", "Price");
f.format("%-15s %5s %10s\n", "----", "---", "-----");
}
public void print(String name, int qty, double price) {
f.format("%-15.15s %5d %10.2f\n", name, qty, price);
total += price;
}
public void printTotal() {
f.format("%-15s %5s %10.2f\n", "Tax", "", total*0.06);
f.format("%-15s %5s %10s\n", "", "", "-----");
f.format("%-15s %5s %10.2f\n", "Total", "",
total * 1.06);
}
public static void main(String[] args) {
Receipt receipt = new Receipt();
receipt.printTitle();
receipt.print("Jack’s Magic Beans", 4, 4.25);
receipt.print("Princess Peas", 3, 5.1);
receipt.print("Three Bears Porridge", 1, 14.29);
receipt.printTotal();
}
} /* Output:
Item Qty Price
---- --- -----
Jack’s Magic Be 4 4.25
Princess Peas 3 5.10
Three Bears Por 1 14.29
Tax 1.42
-----
Total 25.06
*///:~
```

<!--p388-->
Asyou can see, the Formatter provides powerful control over spacing and alignment with fairly concise notation. Here, the format strings are simply copied in order to produce the appropriate spacing. Exercise 4:(3) Modify Receipt.java so that the widths are all controlled by a single set of constant values. The goal is to allow you to easily change a width by changing a single value in one place. Strings
## Formatter conversions
These are the conversions you’ll come across most frequently: Conversion Characters d Integral (as decimal) c Unicode character b Boolean value s String f Floating point (as decimal) e Floating point (in scientific notation) x Integral (as hex) h Hash code (as hex) % Literal "%" Here’s an example that shows these conversions in action:

<!--p389-->
```java
//: strings/Conversion.java
import java.math.*;
import java.util.*;
public class Conversion {
public static void main(String[] args) {
Formatter f = new Formatter(System.out);
char u = ‘a’;
System.out.println("u = ‘a’");
f.format("s: %s\n", u);
// f.format("d: %d\n", u);
f.format("c: %c\n", u);
f.format("b: %b\n", u);
// f.format("f: %f\n", u);
// f.format("e: %e\n", u);
// f.format("x: %x\n", u);
f.format("h: %h\n", u);
int v = 121;
System.out.println("v = 121");
f.format("d: %d\n", v);
f.format("c: %c\n", v);
f.format("b: %b\n", v);
f.format("s: %s\n", v);
// f.format("f: %f\n", v);
// f.format("e: %e\n", v);
f.format("x: %x\n", v);
f.format("h: %h\n", v);
BigInteger w = new BigInteger("50000000000000");
System.out.println(
"w = new BigInteger(\"50000000000000\")");
f.format("d: %d\n", w);
// f.format("c: %c\n", w);
f.format("b: %b\n", w);
f.format("s: %s\n", w);
// f.format("f: %f\n", w);
// f.format("e: %e\n", w);
f.format("x: %x\n", w);
f.format("h: %h\n", w);
double x = 179.543;
System.out.println("x = 179.543");
// f.format("d: %d\n", x);
// f.format("c: %c\n", x);
f.format("b: %b\n", x);
f.format("s: %s\n", x);
f.format("f: %f\n", x);
f.format("e: %e\n", x);
// f.format("x: %x\n", x);
f.format("h: %h\n", x);
Conversion y = new Conversion();
System.out.println("y = new Conversion()");
// f.format("d: %d\n", y);
// f.format("c: %c\n", y);
f.format("b: %b\n", y);
f.format("s: %s\n", y);
// f.format("f: %f\n", y);
// f.format("e: %e\n", y);
// f.format("x: %x\n", y);
f.format("h: %h\n", y);
boolean z = false;
System.out.println("z = false");
// f.format("d: %d\n", z);
// f.format("c: %c\n", z);
f.format("b: %b\n", z);
f.format("s: %s\n", z);
// f.format("f: %f\n", z);
// f.format("e: %e\n", z);
// f.format("x: %x\n", z);
f.format("h: %h\n", z);
}
} /* Output: (Sample)
u = ‘a’
s: a
c: a
b: true
h: 61
v = 121
d: 121
c: y
b: true
s: 121
x: 79
h: 79
w = new BigInteger("50000000000000")
d: 50000000000000
b: true
s: 50000000000000
x: 2d79883d2000
h: 8842a1a7
x = 179.543
b: true
```

<!--p390-->
Strings
```java
s: 179.543
f: 179.543000
e: 1.795430e+02
h: 1ef462c
y = new Conversion()
b: true
s: Conversion@9cab16
h: 9cab16
z = false
b: false
s: false
h: 4d5
*///:~
```
The commented lines show conversions that are invalid for that particular variable type; executing them will trigger an exception. Notice that the ‘b’ conversion works for each variable above. Although it’s valid for any argument type, it might not behave as you’d expect. For boolean primitives or Boolean objects, the result will be true or false, accordingly. However, for any other argument, as long as the argument type is not null the result is always true. Even the numeric value of zero, which is synonymous with false in many languages (including C), will produce true, so be careful when using this conversion with non-boolean types. There are more obscure conversion types and other format specifier options. You can read about these in the JDK documentation for the Formatter class. Exercise 5:(5) For each of the basic conversion types in the above table, write the most complex formatting expression possible. That is, use all the possible format specifiers available for that conversion type.
## String.format()
Java SE5 also took a cue from C’s sprintf( ), which is used to create Strings. String.format( ) is a static method which takes all the same arguments as Formatter’s format( ) but returns a String. It can come in handy when you only need to call format( ) once:

<!--p391-->
```java
//: strings/DatabaseException.java
public class DatabaseException extends Exception {
public DatabaseException(int transactionID, int queryID,
String message) {
super(String.format("(t%d, q%d) %s", transactionID,
queryID, message));
}
public static void main(String[] args) {
try {
throw new DatabaseException(3, 7, "Write failed");
} catch(Exception e) {
System.out.println(e);
}
}
} /* Output:
DatabaseException: (t3, q7) Write failed
*///:~
```
Under the hood, all String.format( ) does is instantiate a Formatter and pass your arguments to it, but using this convenience method can often be clearer and easier than doing it by hand. A hex dump tool As a second example, often you want to look at the bytes inside a binary file using hex format. Here’s a small utility that displays a binary array of bytes in a readable hex format, using String.format( ):
```java
//: net/mindview/util/Hex.java
package net.mindview.util;
import java.io.*;
public class Hex {
public static String format(byte[] data) {
StringBuilder result = new StringBuilder();
int n = 0;
for(byte b : data) {
if(n % 16 == 0)
result.append(String.format("%05X: ", n));
result.append(String.format("%02X ", b));
n++;
if(n % 16 == 0) result.append("\n");
}
result.append("\n");
return result.toString();
}
public static void main(String[] args) throws Exception {
if(args.length == 0)
// Test by displaying this class file:
System.out.println(
format(BinaryFile.read("Hex.class")));
else
System.out.println(
format(BinaryFile.read(new File(args[0]))));
}
} /* Output: (Sample)
00000: CA FE BA BE 00 00 00 31 00 52 0A 00 05 00 22 07
00010: 00 23 0A 00 02 00 22 08 00 24 07 00 25 0A 00 26
00020: 00 27 0A 00 28 00 29 0A 00 02 00 2A 08 00 2B 0A
00030: 00 2C 00 2D 08 00 2E 0A 00 02 00 2F 09 00 30 00
00040: 31 08 00 32 0A 00 33 00 34 0A 00 15 00 35 0A 00
00050: 36 00 37 07 00 38 0A 00 12 00 39 0A 00 33 00 3A
...
*///:~
```

<!--p392-->
To open and read the binary file, this uses another utility that will be introduced in the I/O chapter: net.mindview.util.BinaryFile. The read( ) method returns the entire file as a byte array. Exercise 6:(2) Create a class that contains int, long, float and double fields. Create a toString( ) method for this class that uses String.format( ), and demonstrate that your class works correctly. Strings Regular expressions Regular expressions have long been integral to standard Unix utilities like sed and awk, and languages like Python and Perl (some would argue that they are the predominant reason for Perl’s success). String manipulation tools were previously delegated to the String, StringBuffer, and StringTokenizer classes in Java, which had relatively simple facilities compared to regular expressions. Regular expressions are powerful and flexible text-processing tools. They allow you to specify, programmatically, complex patterns of text that can be discovered in an input string. Once you discover these patterns, you can then react to them any way you want. Although the syntax of regular expressions can be intimidating at first, they provide a compact and dynamic language that can be employed to solve all sorts of string processing, matching and selection, editing, and verification problems in a completely general way. Basics A regular expression is a way to describe strings in general terms, so that you can say, "If a string has these things in it, then it matches what I’m looking for." For example, to say that a number might or might not be preceded by a minus sign, you put in the minus sign followed by a question mark, like this:
```java
-?
```
To describe an integer, you say that it’s one or more digits. In regular expressions, a digit is described by saying ‘\d’. If you have any experience with regular expressions in other languages, you’ll immediately notice a difference in the way backslashes are handled. In other languages, ‘\\’ means "I want to insert a plain old (literal) backslash in the regular expression. Don’t give it any special meaning." In Java, ‘ \ \ ‘ means "I’m inserting a regular expression backslash, so that the following character has special meaning." For example, if you want to indicate a digit, your regular expression string will be ‘\\d’. If you want to insert a literal backslash, you say ‘\\\\’- However, things like newlines and tabs just use a single backslash: ‘\n\t’. To indicate "one or more of the preceding expression," you use a ‘+’. So to say, "possibly a minus sign, followed by one or more digits," you write:
```java
-?\\d+
```
The simplest way to use regular expressions is to use the functionality built into the String class. For example, we can see whether a String matches the regular expression above:

<!--p393-->
```java
//: strings/IntegerMatch.java
public class IntegerMatch {
public static void main(String[] args) {
System.out.println("-1234".matches("-?\\d+"));
System.out.println("5678".matches("-?\\d+"));
System.out.println("+911".matches("-?\\d+"));
System.out.println("+911".matches("(-|\\+)?\\d+"));
}
} /* Output:
true
true
false
true
*///:~
```
The first two expressions match, but the third one starts with a ‘+’, which is a legitimate sign but means the number doesn’t match the regular expression. So we need a way to say, "may start with a + or a -." In regular expressions, parentheses have the effect of grouping an expression, and the vertical bar ‘|’ means OR. So
```java
(-I\\+)?
```
means that this part of the string may be either a ‘-’ or a ‘+’ or nothing (because of the ‘?’). Because the ‘+’ character has special meaning in regular expressions, it must be escaped with a ‘\\’ in order to appear as an ordinary character in the expression. A useful regular expression tool that’s built into String is split( ), which means, "Split this string around matches of the given regular expression."
```java
//: strings/Splitting.java
import java.util.*;
public class Splitting {
public static String knights =
"Then, when you have found the shrubbery, you must " +
"cut down the mightiest tree in the forest... " +
"with... a herring!";
public static void split(String regex) {
System.out.println(
Arrays.toString(knights.split(regex)));
}
public static void main(String[] args) {
split(" "); // Doesn’t have to contain regex chars
split("\\W+"); // Non-word characters
split("n\\W+"); // ‘n’ followed by non-word characters
}
} /* Output:
[Then,, when, you, have, found, the, shrubbery,, you, must, cut, down,
the, mightiest, tree, in, the, forest..., with..., a, herring!]
[Then, when, you, have, found, the, shrubbery, you, must, cut, down,
the, mightiest, tree, in, the, forest, with, a, herring]
[The, whe, you have found the shrubbery, you must cut dow, the mightiest
tree i, the forest... with... a herring!]
*///:~
```
First, note that you may use ordinary characters as regular expressions—a regular expression doesn’t have to contain special characters, as you can see in the first call to split( ), which just splits on whitespace. The second and third calls to split( ) use ‘\W’, which means a non-word character (the lowercase version, ‘\w’, means a word character)—you can see that the punctuation has been removed in the second case. The third call to split( ) says, "the letter n followed by one or more non-word characters." You can see that the split patterns do not appear in the result. An overloaded version of String. split( ) allows you to limit the number of splits that occur. The final regular expression tool built into String is replacement. You can either replace the first occurrence, or all of them:
```java
//: strings/Replacing.java
import static net.mindview.util.Print.*;
public class Replacing {
static String s = Splitting.knights;
public static void main(String[] args) {
```

<!--p394-->
Strings
```java
print(s.replaceFirst("f\\w+", "located"));
print(s.replaceAll("shrubbery|tree|herring","banana"));
}
} /* Output:
Then, when you have located the shrubbery, you must cut down the
mightiest tree in the forest... with... a herring!
Then, when you have found the banana, you must cut down the mightiest
banana in the forest... with... a banana!
*///:~
```

<!--p395-->
The first expression matches the letter f followed by one or more word characters (note that the w is lowercase this time). It only replaces the first match that it finds, so the word "found" is replaced by the word "located." The second expression matches any of the three words separated by the OR vertical bars, and it replaces all matches that it finds. You’ll see that the non-String regular expressions have more powerful replacement tools— for example, you can call methods to perform replacements. Non-String regular expressions are also significantly more efficient if you need to use the regular expression more than once. Exercise 7:(5) Using the documentation for java.util.regex.Pattern as a resource, write and test a regular expression that checks a sentence to see that it begins with a capital letter and ends with a period. Exercise 8:(2) Split the string Splitting.knights on the words "the" or “you." Exercise 9:(4) Using the documentation for java.util.regex.Pattern as a resource, replace all the vowels in Splitting.knights with underscores. Creating regular expressions You can begin learning regular expressions with a subset of the possible constructs. A complete list of constructs for building regular expressions can be found in the JDK documentation for the Pattern class for package java.util.regex. Characters B The specific character B \xhh Character with hex value oxhh \uhhhh The Unicode character with hex representation 0xhhhh \t Tab \n Newline \r Carriage return \f Form feed \e Escape The power of regular expressions begins to appear when you are defining character classes. Here are some typical ways to create character classes, and some predefined classes: Character Classes . Any character [abc] Any of the characters a, b, or c (same as a|b|c) [^abc] Any character except a, b, and c (negation) [a-zA-Z] Any character a through z or A through Z (range) [abc[hij]] Any of a,b,c,h,I,j (same as a|b|c|h|i|j) (union) [a-z&&[hij]] Either h, i, or j (intersection) \s A whitespace character (space, tab, newline, form feed, carriage return) \S A non-whitespace character ([^\s]) \d A numeric digit [0-9] \D A non-digit [^o-9] \w A word character [a-zA-Z_0-9] \W A non-word character [^\w] What’s shown here is only a sample; you’ll want to bookmark the JDK documentation page for java.util.regex.Pattern so you can easily access all the possible regular expression patterns. Logical Operators XY X followed by Y X|Y X or Y (X) A capturing group. You can refer to the ith captured group later in the expression with \i. Boundary Matchers ^ Beginning of a line $ End of a line \b Word boundary \B Non-word boundary \G End of the previous match As an example, each of the following successfully matches the character sequence "Rudolph":
```java
//: strings/Rudolph.java
public class Rudolph {
public static void main(String[] args) {
for(String pattern : new String[]{ "Rudolph",
"[rR]udolph", "[rR][aeiou][a-z]ol.*", "R.*" })
System.out.println("Rudolph".matches(pattern));
```

<!--p396-->
Strings
```java
}
} /* Output:
true
true
true
true
*///:~
```
Of course, your goal should not be to create the most obfuscated regular expression, but rather the simplest one necessary to do the job. You’ll find that, once you start writing regular expressions, you’ll often use your code as a reference when writing new regular expressions. Quantifiers A quantifier describes the way that a pattern absorbs input text: • Greedy: Quantifiers are greedy unless otherwise altered. A greedy expression finds as many possible matches for the pattern as possible. A typical cause of problems is to assume that your pattern will only match the first possible group of characters, when it’s actually greedy and will keep going until it’s matched the largest possible string. • Reluctant: Specified with a question mark, this quantifier matches the minimum number of characters necessary to satisfy the pattern. Also called lazy, minimal matching, non-greedy, or ungreedy. • Possessive: Currently this is only available in Java (not in other languages) and is more advanced, so you probably won’t use it right away. As a regular expression is applied to a string, it generates many states so that it can backtrack if the match fails. Possessive quantifiers do not keep those intermediate states, and thus prevent backtracking. They can be used to prevent a regular expression from running away and also to make it execute more efficiently. Greedy Reluctant Possessive Matches X? X?? X?+ X, one or none X* X*? x*+ X, zero or more x+ x+? X++ X, one or more X{n} X{n}? X{n}+ X, exactly n times X{n,} X{n,}? X{n,}+ X, at least n times X{n,m} X{n,m}? X{n,m}+ X, at least n but not more than m times Keep in mind that the expression ‘X’ will often need to be surrounded in parentheses for it to work the way you desire. For example:
```java
abc+
```

<!--p397-->
might seem like it would match the sequence ‘abc’ one or more times, and if you apply it to the input string ‘abcabcabc’, you will in fact get three matches. However, the expression actually says, "Match ‘ab’ followed by one or more occurrences of ‘c’." To match the entire string ‘abc’ one or more times, you must say:
```java
(abc)+
```
You can easily be fooled when using regular expressions; it’s an orthogonal language, on top of Java.
## CharSequence
The interface called CharSequence establishes a generalized definition of a character sequence abstracted from the CharBuffer, String, StringBuffer, or StringBuilder classes:
```java
interface CharSequence {
charAt(int i);
length();
subSequence(int start,| int end);
toString();
}
```
The aforementioned classes implement this interface. Many regular expression operations take CharSequence arguments.
## Pattern and Matcher
In general, you’ll compile regular expression objects rather than using the fairly limited String utilities. To do this, you import java.util.regex, then compile a regular expression by using the static Pattern.compile( ) method. This produces a Pattern object based on its String argument. You use the Pattern by calling the matcher( ) method, passing the string that you want to search. The matcher( ) method produces a Matcher object, which has a set of operations to choose from (you can see all of these in the JDK documentation for java.util.regex.Matcher). For example, the replaceAll( ) method replaces all the matches with its argument. As a first example, the following class can be used to test regular expressions against an input string. The first command-line argument is the input string to match against, followed by one or more regular expressions to be applied to the input. Under Unix/Linux, the regular expressions must be quoted on the command line. This program can be useful in testing regular expressions as you construct them to see that they produce your intended matching behavior.
```java
//: strings/TestRegularExpression.java
// Allows you to easily try out regular expressions.
// {Args: abcabcabcdefabc "abc+" "(abc)+" "(abc){2,}" }
import java.util.regex.*;
import static net.mindview.util.Print.*;
public class TestRegularExpression {
public static void main(String[] args) {
if(args.length < 2) {
print("Usage:\njava TestRegularExpression " +
"characterSequence regularExpression+");
System.exit(0);
}
print("Input: \"" + args[0] + "\"");
for(String arg : args) {
print("Regular expression: \"" + arg + "\"");
Pattern p = Pattern.compile(arg);
Matcher m = p.matcher(args[0]);
while(m.find()) {
```

<!--p398-->
Strings
```java
print("Match \"" + m.group() + "\" at positions " +
m.start() + "-" + (m.end() - 1));
}
}
}
} /* Output:
Input: "abcabcabcdefabc"
Regular expression: "abcabcabcdefabc"
Match "abcabcabcdefabc" at positions 0-14
Regular expression: "abc+"
Match "abc" at positions 0-2
Match "abc" at positions 3-5
Match "abc" at positions 6-8
Match "abc" at positions 12-14
Regular expression: "(abc)+"
Match "abcabcabc" at positions 0-8
Match "abc" at positions 12-14
Regular expression: "(abc){2,}"
Match "abcabcabc" at positions 0-8
*///:~
```
A Pattern object represents the compiled version of a regular expression. As seen in the preceding example, you can use the matcher( ) method and the input string to produce a Matcher object from the compiled Pattern object. Pattern also has a static method:
```java
static boolean matches(String regex, CharSequence input)
```
to check whether regex matches the entire input CharSequence, and a split( ) method that produces an array of String that has been broken around matches of the regex. A Matcher object is generated by calling Pattern.matcher( ) with the input string as an argument. The Matcher object is then used to access the results, using methods to evaluate the success or failure of different types of matches:
```java
boolean matches()
boolean lookingAt()
boolean find()
boolean find(int start)
```
The matches ( ) method is successful if the pattern matches the entire input string, while lookingAt( ) is successful if the input string, starting at the beginning, is a match to the pattern. Exercise 10:(2) For the phrase "Java now has regular expressions" evaluate whether the following expressions will find a match:

<!--p399-->
```java
^Java
\Breg.*
n.w\s+h(a|i)s
s?
s*
s+
s{4}
S{1}.
s{0,3}
```
Exercise 11:(2) Apply the regular expression
```java
(?i)((^[aeiou])|(\s+[aeiou]))\w+?[aeiou]\b
```
to
```java
"Arline ate eight apples and one orange while Anita hadn’t any"
```
## find()
Matcher.find( ) can be used to discover multiple pattern matches in the CharSequence to which it is applied. For example:
```java
//: strings/Finding.java
import java.util.regex.*;
import static net.mindview.util.Print.*;
public class Finding {
public static void main(String[] args) {
Matcher m = Pattern.compile("\\w+")
.matcher("Evening is full of the linnet’s wings");
while(m.find())
printnb(m.group() + " ");
print();
int i = 0;
while(m.find(i)) {
printnb(m.group() + " ");
i++;
}
}
} /* Output:
Evening is full of the linnet s wings
Evening vening ening ning ing ng g is is s full full ull ll l of of f
the the he e linnet linnet innet nnet net et t s s wings wings ings ngs
gs s
*///:~
```
The pattern ‘\\w+’ splits the input into words. find( ) is like an iterator, moving forward through the input string. However, the second version of find( ) can be given an integer argument that tells it the character position for the beginning of the search—this version resets the search position to the value of the argument, as you can see from the output. Groups Groups are regular expressions set off by parentheses that can be called up later with their group number. Group o indicates the whole expression match, group l is the first parenthesized group, etc. Thus in
```java
A(B(C))D
```

<!--p400-->
there are three groups: Group 0 is ABCD, group 1 is BC, and group 2 is C. The Matcher object has methods to give you information about groups: public int groupCount( ) returns the number of groups in this matcher’s pattern. Group o is not included in this count. Strings public String group( ) returns group 0 (the entire match) from the previous match operation (find( ), for example). public String group(int i) returns the given group number during the previous match operation. If the match was successful, but the group specified failed to match any part of the input string, then null is returned. public int start(int group) returns the start index of the group found in the previous match operation. public int end(int group) returns the index of the last character, plus one, of the group found in the previous match operation. Here’s an example:
```java
//: strings/Groups.java
import java.util.regex.*;
import static net.mindview.util.Print.*;
public class Groups {
static public final String POEM =
"Twas brillig, and the slithy toves\n" +
"Did gyre and gimble in the wabe.\n" +
"All mimsy were the borogoves,\n" +
"And the mome raths outgrabe.\n\n" +
"Beware the Jabberwock, my son,\n" +
"The jaws that bite, the claws that catch.\n" +
"Beware the Jubjub bird, and shun\n" +
"The frumious Bandersnatch.";
public static void main(String[] args) {
Matcher m =
Pattern.compile("(?m)(\\S+)\\s+((\\S+)\\s+(\\S+))$")
.matcher(POEM);
while(m.find()) {
for(int j = 0; j <= m.groupCount(); j++)
printnb("[" + m.group(j) + "]");
print();
}
}
} /* Output:
[the slithy toves][the][slithy toves][slithy][toves]
[in the wabe.][in][the wabe.][the][wabe.]
[were the borogoves,][were][the borogoves,][the][borogoves,]
[mome raths outgrabe.][mome][raths outgrabe.][raths][outgrabe.]
[Jabberwock, my son,][Jabberwock,][my son,][my][son,]
[claws that catch.][claws][that catch.][that][catch.]
[bird, and shun][bird,][and shun][and][shun]
[The frumious Bandersnatch.][The][frumious
Bandersnatch.][frumious][Bandersnatch.]
*///:~
```

<!--p401-->
The poem is the first part of Lewis Carroll’s "Jabberwocky," from Through the Looking Glass. You can see that the regular expression pattern has a number of parenthesized groups, consisting of any number of non-whitespace characters (‘\S+’) followed by any number of whitespace characters (‘\s+’). The goal is to capture the last three words on each line; the end of a line is delimited by ‘$’. However, the normal behavior is to match ‘$’ with the end of the entire input sequence, so you must explicitly tell the regular expression to pay attention to newlines within the input. This is accomplished with the ‘(?m)’ pattern flag at the beginning of the sequence (pattern flags will be shown shortly). Strings Exercise 12:(5) Modify Groups.java to count all of the unique words that do not start with a capital letter.
## start() and end()
Following a successful matching operation, start( ) returns the start index of the previous match, and end( ) returns the index of the last character matched, plus one. Invoking either start( ) or end( ) following an unsuccessful matching operation (or before attempting a matching operation) produces an IllegalStateException. The following program also demonstrates matches( ) and lookingAt( ):3
```java
//: strings/StartEnd.java
import java.util.regex.*;
import static net.mindview.util.Print.*;
public class StartEnd {
public static String input =
"As long as there is injustice, whenever a\n" +
"Targathian baby cries out, wherever a distress\n" +
"signal sounds among the stars ... We’ll be there.\n" +
"This fine ship, and this fine crew ...\n" +
"Never give up! Never surrender!";
private static class Display {
private boolean regexPrinted = false;
private String regex;
Display(String regex) { this.regex = regex; }
void display(String message) {
if(!regexPrinted) {
print(regex);
regexPrinted = true;
}
print(message);
}
}
static void examine(String s, String regex) {
Display d = new Display(regex);
Pattern p = Pattern.compile(regex);
Matcher m = p.matcher(s);
while(m.find())
d.display("find() ‘" + m.group() +
"‘ start = "+ m.start() + " end = " + m.end());
if(m.lookingAt()) // No reset() necessary
d.display("lookingAt() start = "
+ m.start() + " end = " + m.end());
if(m.matches()) // No reset() necessary
d.display("matches() start = "
+ m.start() + " end = " + m.end());
}
public static void main(String[] args) {
for(String in : input.split("\n")) {
print("input : " + in);
for(String regex : new String[]{"\\w*ere\\w*",
"\\w*ever", "T\\w+", "Never.*?!"})
examine(in, regex);
}
}
} /* Output:
input : As long as there is injustice, whenever a
```

<!--p402-->
3Quote from one of Commander Taggart’s speeches on Galaxy Quest.
```java
\w*ere\w*
find() ‘there’ start = 11 end = 16
\w*ever
find() ‘whenever’ start = 31 end = 39
input : Targathian baby cries out, wherever a distress
\w*ere\w*
find() ‘wherever’ start = 27 end = 35
\w*ever
find() ‘wherever’ start = 27 end = 35
T\w+
find() ‘Targathian’ start = 0 end = 10
lookingAt() start = 0 end = 10
input : signal sounds among the stars ... We’ll be there.
\w*ere\w*
find() ‘there’ start = 43 end = 48
input : This fine ship, and this fine crew ...
T\w+
find() ‘This’ start = 0 end = 4
lookingAt() start = 0 end = 4
input : Never give up! Never surrender!
\w*ever
find() ‘Never’ start = 0 end = 5
find() ‘Never’ start = 15 end = 20
lookingAt() start = 0 end = 5
Never.*?!
find() ‘Never give up!’ start = 0 end = 14
find() ‘Never surrender!’ start = 15 end = 31
lookingAt() start = 0 end = 14
matches() start = 0 end = 31
*///:~
```
Notice that find( ) will locate the regular expression anywhere in the input, but lookingAt( ) and matches( ) only succeed if the regular expression starts matching at the very beginning of the input. While matches( ) only succeeds if the entire input matches the regular expression, lookingAt( )4 succeeds if only the first part of the input matches. Exercise 13:(2) Modify StartEnd.java so that it uses Groups.POEM as input, but still produces positive outputs for find( ), lookingAt( ) and matches( ).
## Pattern flags
An alternative compile( ) method accepts flags that affect matching behavior:
```java
Pattern Pattern.compile(String regex, int flag)
```

<!--p403-->

<!--p404-->
where flag is drawn from among the following Pattern class constants: 4I have no idea how they came up with this method name, or what it’s supposed to refer to. But it’s reassuring to know that whoever comes up with nonintuitive method names is still employed at Sun. And that their apparent policy of not reviewing code designs is still in place. Sorry for the sarcasm, but this kind of thing gets tiresome after a few years. Compile Flag Effect Pattern.CANON_EQ Two characters will be considered to match if, and only if, their full canonical decompositions match. The expression ‘\u003F’, for example, will match the string ‘?’ when this flag is specified. By default, matching does not take canonical equivalence into account. Pattern.CASE INSENSITIVE (?i) By default, case-insensitive matching assumes that only characters in the US- ASCII character set are being matched. This flag allows your pattern to match without regard to case (upper or lower). Unicode-aware case-insensitive matching can be enabled by specifying the UNICODE_CASE flag in conjunction with this flag. Pattern.COMMENTS (?x) In this mode, whitespace is ignored, and embedded comments starting with # are ignored until the end of a line. Unix lines mode can also be enabled via the embedded flag expression. Pattern.DOTALL (?s) In dotall mode, the expression’.’ matches any character, including a line terminator. By default, the ‘.’ expression does not match line terminators. Pattern.MULTILINE (?m) In multiline mode, the expressions ‘^’ and ‘$’ match the beginning and ending of a line, respectively.’^’ also matches the beginning of the input string, and ‘$’ also matches the end of the input string. By default, these expressions only match at the beginning and the end of the entire input string. Pattern.UNICODE CASE (?u) Case-insensitive matching, when enabled by the CASE_INSENSITIVE flag, is done in a manner consistent with the Unicode Standard. By default, case- insensitive matching assumes that only characters in the US-ASCII character set are being matched. Pattern.UNIX LINES (?d) In this mode, only the ‘\n’ line terminator is recognized in the behavior of ‘.’, ‘^’, and ‘$’. Particularly useful among these flags are Pattern.CASE_INSENSITIVE, Pattern.MULTILINE, and Pattern.COMMENTS (which is helpful for clarity and/or documentation). Note that the behavior of most of the flags can also be obtained by inserting the parenthesized characters, shown beneath the flags in the table, into your regular expression preceding the place where you want the mode to take effect. Strings You can combine the effect of these and other flags through an "OR" (‘|’) operation:
```java
//: strings/ReFlags.java
import java.util.regex.*;
public class ReFlags {
public static void main(String[] args) {
Pattern p = Pattern.compile("^java",
Pattern.CASE_INSENSITIVE | Pattern.MULTILINE);
Matcher m = p.matcher(
"java has regex\nJava has regex\n" +
"JAVA has pretty good regular expressions\n" +
"Regular expressions are in Java");
while(m.find())
System.out.println(m.group());
}
} /* Output:
java
Java
JAVA
*///:~
```
This creates a pattern that will match lines starting with "Java," "Java," "JAVA," etc., and attempt a match for each line within a multiline set (matches starting at the beginning of the character sequence and following each line terminator within the character sequence). Note that the group( ) method only produces the matched portion.
## split()
split( ) divides an input string into an array of String objects, delimited by the regular expression.
```java
String[] split(CharSequence input)
String[] split(CharSequence input, int limit)
```
This is a handy way to break input text on a common boundary:
```java
//: strings/SplitDemo.java
import java.util.regex.*;
import java.util.*;
import static net.mindview.util.Print.*;
public class SplitDemo {
public static void main(String[] args) {
String input =
"This!!unusual use!!of exclamation!!points";
print(Arrays.toString(
Pattern.compile("!!").split(input)));
// Only do the first three:
print(Arrays.toString(
Pattern.compile("!!").split(input, 3)));
}
} /* Output:
[This, unusual use, of exclamation, points]
[This, unusual use, of exclamation!!points]
*///:~
```

<!--p405-->
The second form of split( ) limits the number of splits that occur. Exercise 14:(1) Rewrite SplitDemo using String.split( ). Replace operations Regular expressions are especially useful to replace text. Here are the available methods: replaceFirst(String replacement) replaces the first matching part of the input string with replacement. replaceAll(String replacement) replaces every matching part of the input string with replacement. appendReplacement(StringBuffer sbuf, String replacement) performs step-by-step replacements into sbuf, rather than replacing only the first one or all of them, as in replaceFirst( ) and replaceAll( ), respectively. This is a very important method, because it allows you to call methods and perform other processing in order to produce replacement (replaceFirst( ) and replaceAll( ) are only able to put in fixed strings). With this method, you can programmatically pick apart the groups and create powerful replacements. appendTail(StringBuffer sbuf, String replacement) is invoked after one or more invocations of the appendReplacement( ) method in order to copy the remainder of the input string. Here’s an example that shows the use of all the replace operations. The block of commented text at the beginning is extracted and processed with regular expressions for use as input in the rest of the example:
```java
//: strings/TheReplacements.java
import java.util.regex.*;
import net.mindview.util.*;
import static net.mindview.util.Print.*;
/*! Here’s a block of text to use as input to
the regular expression matcher. Note that we’ll
first extract the block of text by looking for
the special delimiters, then process the
extracted block. !*/
public class TheReplacements {
public static void main(String[] args) throws Exception {
String s = TextFile.read("TheReplacements.java");
// Match the specially commented block of text above:
Matcher mInput =
Pattern.compile("/\\*!(.*)!\\*/", Pattern.DOTALL)
.matcher(s);
if(mInput.find())
s = mInput.group(1); // Captured by parentheses
// Replace two or more spaces with a single space:
s = s.replaceAll(" {2,}", " ");
// Replace one or more spaces at the beginning of each
// line with no spaces. Must enable MULTILINE mode:
s = s.replaceAll("(?m)^ +", "");
print(s);
s = s.replaceFirst("[aeiou]", "(VOWEL1)");
StringBuffer sbuf = new StringBuffer();
Pattern p = Pattern.compile("[aeiou]");
Matcher m = p.matcher(s);
// Process the find information as you
```

<!--p406-->
Strings
```java
// perform the replacements:
while(m.find())
m.appendReplacement(sbuf, m.group().toUpperCase());
// Put in the remainder of the text:
m.appendTail(sbuf);
print(sbuf);
}
} /* Output:
Here’s a block of text to use as input to
the regular expression matcher. Note that we’ll
first extract the block of text by looking for
the special delimiters, then process the
extracted block.
H(VOWEL1)rE’s A blOck Of tExt tO UsE As InpUt tO
thE rEgUlAr ExprEssIOn mAtchEr. NOtE thAt wE’ll
fIrst ExtrAct thE blOck Of tExt by lOOkIng fOr
thE spEcIAl dElImItErs, thEn prOcEss thE
ExtrActEd blOck.
*///:~
```
The file is opened and read using the TextFile class in the net.mindview.util library (the code for this will be shown in the I/O chapter). The static read( ) method reads the entire file and returns it as a String. mInput is created to match all the text (notice the grouping parentheses) between ‘/*!’ and ‘!*/’. Then, more than two spaces are reduced to a single space, and any space at the beginning of each line is removed (in order to do this on all lines and not just the beginning of the input, multiline mode must be enabled). These two replacements are performed with the equivalent (but more convenient, in this case) replaceAll( ) that’s part of String. Note that since each replacement is only used once in the program, there’s no extra cost to doing it this way rather than precompiling it as a Pattern. replaceFirst( ) only performs the first replacement that it finds. In addition, the replacement strings in replaceFirst( ) and replaceAll( ) are just literals, so if you want to perform some processing on each replacement, they don’t help. In that case, you need to use appendReplacement( ), which allows you to write any amount of code in the process of performing the replacement. In the preceding example, a group( ) is selected and processed—in this situation, setting the vowel found by the regular expression to uppercase— as the resulting sbuf is being built. Normally, you step through and perform all the replacements and then call appendTail( ), but if you want to simulate replaceFirst( ) (or "replace n"), you just do the replacement one time and then call appendTail( ) to put the rest into sbuf. appendReplacement( ) also allows you to refer to captured groups directly in the replacement string by saying "$g", where ‘g’ is the group number. However, this is for simpler processing and wouldn’t give you the desired results in the preceding program.
## reset()
An existing Matcher object can be applied to a new character sequence using the reset( ) methods:

<!--p407-->
```java
//: strings/Resetting.java
import java.util.regex.*;
public class Resetting {
public static void main(String[] args) throws Exception {
Matcher m = Pattern.compile("[frb][aiu][gx]")
.matcher("fix the rug with bags");
while(m.find())
System.out.print(m.group() + " ");
System.out.println();
m.reset("fix the rig with rags");
while(m.find())
System.out.print(m.group() + " ");
}
} /* Output:
fix rug bag
fix rig rag
*///:~
```
reset( ) without any arguments sets the Matcher to the beginning of the current sequence. Regular expressions and Java I/O Most of the examples so far have shown regular expressions applied to static strings. The following example shows one way to apply regular expressions to search for matches in a file. Inspired by Unix’s grep, JGrep.java takes two arguments: a file name and the regular expression that you want to match. The output shows each line where a match occurs and the match position(s) within the line.
```java
//: strings/JGrep.java
// A very simple version of the "grep" program.
// {Args: JGrep.java "\\b[Ssct]\\w+"}
import java.util.regex.*;
import net.mindview.util.*;
public class JGrep {
public static void main(String[] args) throws Exception {
if(args.length < 2) {
System.out.println("Usage: java JGrep file regex");
System.exit(0);
}
Pattern p = Pattern.compile(args[1]);
// Iterate through the lines of the input file:
int index = 0;
Matcher m = p.matcher("");
for(String line : new TextFile(args[0])) {
m.reset(line);
while(m.find())
System.out.println(index++ + ": " +
m.group() + ": " + m.start());
}
}
} /* Output: (Sample)
0: strings: 4
1: simple: 10
2: the: 28
3: Ssct: 26
4: class: 7
5: static: 9
6: String: 26
7: throws: 41
8: System: 6
9: System: 6
10: compile: 24
11: through: 15
12: the: 23
13: the: 36
14: String: 8
15: System: 8
```

<!--p408-->
Strings
```java
16: start: 31
*///:~
```
The file is opened as a net.mindview.util.TextFile object (which will be shown in the I/O chapter), which reads the lines of the file into an ArrayList. This means that the foreach syntax can iterate through the lines in the TextFile object. Although it’s possible to create a new Matcher object within the for loop, it is slightly more optimal to create an empty Matcher object outside the loop and use the reset( ) method to assign each line of the input to the Matcher. The result is scanned with find( ). The test arguments open the JGrep.java file to read as input, and search for words starting with [Ssct]. You can learn much more about regular expressions in Mastering Regular Expressions, 2nd Edition, by Jeffrey E. F. Friedl (O’Reilly, 2002). There are also numerous introductions to regular expressions on the Internet, and you can often find helpful information in the documentation for languages like Perl and Python. Exercise 15:(5) Modify JGrep.java to accept flags as arguments (e.g., Pattern.CASE_INSENSITIVE, Pattern.MULTILINE). Exercise 16:(5) Modify JGrep.java to accept a directory name or a file name as argument (if a directory is provided, search should include all files in the directory). Hint: You can generate a list of file names with:
```java
File[] files = new File(".").listFiles();
```
Exercise 17:(8) Write a program that reads a Java source-code file (you provide the file name on the command line) and displays all the comments. Exercise 18:(8) Write a program that reads a Java source-code file (you provide the file name on the command line) and displays all the string literals in the code. Exercise 19:(8) Building on the previous two exercises, write a program that examines Java source code and produces all the class names used in a particular program. Scanning input Until now it has been relatively painful to read data from a human-readable file or from standard input. The usual solution is to read in a line of text, tokenize it, and then use the various parse methods of Integer, Double, etc., to parse the data:

<!--p409-->
```java
//: strings/SimpleRead.java
import java.io.*;
public class SimpleRead {
public static BufferedReader input = new BufferedReader(
new StringReader("Sir Robin of Camelot\n22 1.61803"));
public static void main(String[] args) {
try {
System.out.println("What is your name?");
String name = input.readLine();
System.out.println(name);
System.out.println(
"How old are you? What is your favorite double?");
System.out.println("(input: <age> <double>)");
String numbers = input.readLine();
System.out.println(numbers);
String[] numArray = numbers.split(" ");
int age = Integer.parseInt(numArray[0]);
double favorite = Double.parseDouble(numArray[1]);
System.out.format("Hi %s.\n", name);
System.out.format("In 5 years you will be %d.\n",
age + 5);
System.out.format("My favorite double is %f.",
favorite / 2);
} catch(IOException e) {
System.err.println("I/O exception");
}
}
} /* Output:
What is your name?
Sir Robin of Camelot
How old are you? What is your favorite double?
(input: <age> <double>)
22 1.61803
Hi Sir Robin of Camelot.
In 5 years you will be 27.
My favorite double is 0.809015.
*///:~
```
The input field uses classes from java.io, which will not officially be introduced until the I/O chapter. A StringReader turns a String into a readable stream, and this object is used to create a BufferedReader because BufferedReader has a readLine( ) method. The result is that the input object can be read a line at a time, just as if it were standard input from the console. readLine( ) is used to get the String for each line of input. It’s fairly straightforward when you want to get one input for each line of data, but if two input values are on a single line, things get messy—the line must be split so we can parse each input separately. Here, the splitting takes place when creating numArray, but note that the split( ) method was introduced in J2SE1.4, so before that you had to do something else. The Scanner class, added in Java SE5, relieves much of the burden of scanning input:
```java
//: strings/BetterRead.java
import java.util.*;
public class BetterRead {
public static void main(String[] args) {
Scanner stdin = new Scanner(SimpleRead.input);
System.out.println("What is your name?");
String name = stdin.nextLine();
System.out.println(name);
System.out.println(
"How old are you? What is your favorite double?");
System.out.println("(input: <age> <double>)");
int age = stdin.nextInt();
double favorite = stdin.nextDouble();
System.out.println(age);
System.out.println(favorite);
System.out.format("Hi %s.\n", name);
System.out.format("In 5 years you will be %d.\n",
age + 5);
System.out.format("My favorite double is %f.",
favorite / 2);
```

<!--p410-->
Strings
```java
}
} /* Output:
What is your name?
Sir Robin of Camelot
How old are you? What is your favorite double?
(input: <age> <double>)
1.61803
Hi Sir Robin of Camelot.
In 5 years you will be 27.
My favorite double is 0.809015.
*///:~
```
The Scanner constructor can take just about any kind of input object, including a File object (which will also be covered in the I/O chapter), an InputStream, a String, or in this case a Readable, which is an interface introduced in Java SE5 to describe "something that has a read( ) method." The BufferedReader from the previous example falls into this category. With Scanner, the input, tokenizing, and parsing are all ensconced in various different kinds of "next" methods. A plain next( ) returns the next String token, and there are "next" methods for all the primitive types (except char)as well as for BigDecimal and Biglnteger. All of the "next" methods block, meaning they will return only after a complete data token is available for input. There are also corresponding "hasNext" methods that return true if the next input token is of the correct type. An interesting difference between the two previous examples above is the lack of a try block for IOExceptions in BetterRead.java. One of the assumptions made by the Scanner is that an IOException signals the end of input, and so these are swallowed by the Scanner. However, the most recent exception is available through the ioException( ) method, so you are able to examine it if necessary. Exercise 20:(2) Create a class that contains int, long, float and double and String fields. Create a constructor for this class that takes a single String argument, and scans that string into the various fields. Add a toString( ) method and demonstrate that your class works correctly.
## Scanner delimiters
By default, a Scanner splits input tokens along whitespace, but you can also specify your own delimiter pattern in the form of a regular expression:

<!--p411-->
```java
//: strings/ScannerDelimiter.java
import java.util.*;
public class ScannerDelimiter {
public static void main(String[] args) {
Scanner scanner = new Scanner("12, 42, 78, 99, 42");
scanner.useDelimiter("\\s*,\\s*");
while(scanner.hasNextInt())
System.out.println(scanner.nextInt());
}
} /* Output:
*///:~
```
This example uses commas (surrounded by arbitrary amounts of whitespace) as the delimiter when reading from the given String. This same technique can be used to read from comma- delimited files. In addition to useDelimiter( ) for setting the delimiter pattern, there is also delimiter( ), which returns the current Pattern being used as a delimiter. Scanning with regular expressions In addition to scanning for predefined primitive types, you can also scan for your own user- defined patterns, which is helpful when scanning more complex data. This example scans threat data from a log like your firewall might produce:
```java
//: strings/ThreatAnalyzer.java
import java.util.regex.*;
import java.util.*;
public class ThreatAnalyzer {
static String threatData =
"58.27.82.161@02/10/2005\n" +
"204.45.234.40@02/11/2005\n" +
"58.27.82.161@02/11/2005\n" +
"58.27.82.161@02/12/2005\n" +
"58.27.82.161@02/12/2005\n" +
"[Next log section with different data format]";
public static void main(String[] args) {
Scanner scanner = new Scanner(threatData);
String pattern = "(\\d+[.]\\d+[.]\\d+[.]\\d+)@" +
"(\\d{2}/\\d{2}/\\d{4})";
while(scanner.hasNext(pattern)) {
scanner.next(pattern);
MatchResult match = scanner.match();
String ip = match.group(1);
String date = match.group(2);
System.out.format("Threat on %s from %s\n", date,ip);
}
}
} /* Output:
Threat on 02/10/2005 from 58.27.82.161
Threat on 02/11/2005 from 204.45.234.40
Threat on 02/11/2005 from 58.27.82.161
Threat on 02/12/2005 from 58.27.82.161
Threat on 02/12/2005 from 58.27.82.161
*///:~
```
When you use next( ) with a specific pattern, that pattern is matched against the next input token. The result is made available by the match( ) method, and as you can see above, it works just like the regular expression matching you saw earlier. There’s one caveat when scanning with regular expressions. The pattern is matched against the next input token only, so if your pattern contains a delimiter it will never be matched.
## StringTokenizer
Before regular expressions (in J2SE1.4) or the Scanner class (in Java SE5), the way to split a string into parts was to "tokenize" it with StringTokenizer. But now it’s much easier and more succinct to do the same thing with regular expressions or the Scanner class. Here’s a simple comparison of StringTokenizer to the other two techniques:
```java
//: strings/ReplacingStringTokenizer.java
```

<!--p412-->
Strings
```java
import java.util.*;
public class ReplacingStringTokenizer {
public static void main(String[] args) {
String input = "But I’m not dead yet! I feel happy!";
StringTokenizer stoke = new StringTokenizer(input);
while(stoke.hasMoreElements())
System.out.print(stoke.nextToken() + " ");
System.out.println();
System.out.println(Arrays.toString(input.split(" ")));
Scanner scanner = new Scanner(input);
while(scanner.hasNext())
System.out.print(scanner.next() + " ");
}
} /* Output:
But I’m not dead yet! I feel happy!
[But, I’m, not, dead, yet!, I, feel, happy!]
But I’m not dead yet! I feel happy!
*///:~
```

<!--p413-->
With regular expressions or Scanner objects, you can also split a string into parts using more complex patterns—something that’s difficult with StringTokenizer. Itseems safe to say that the StringTokenizer is obsolete. Strings Summary In the past, Java support for string manipulation was rudimentary, but in recent editions of the language we’ve seen far more sophisticated support adopted from other languages. At this point, the support for strings is reasonably complete, although you must sometimes pay attention to efficiency details such as the appropriate use of StringBuilder. Solutions to selected exercises can be found in the electronic document The Thinking in Java Annotated Solution Guide, available for sale from www.MindView.net.