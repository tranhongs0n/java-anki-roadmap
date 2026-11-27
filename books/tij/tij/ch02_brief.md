# 2. Everything Is an Object (printed p41-62)


<!--p63-->

<!--p64-->
```java
String s;
```
```java
String s = "asdf";
```
```java
String s = new String("asdf");
```

<!--p65-->

<!--p66-->
```java
char c = ‘x’;
Character ch = new Character(c);
```
```java
Character ch = new Character(‘x’);
```
```java
Character ch = ‘x’;
```
```java
char c = ch;
```

<!--p67-->
```java
{
int x = 12;
// Only x available
{
int q = 96;
// Both x & q available
}
// Only x available
// q is "out of scope"
}
```
```java
{
int x = 12;
{
```

<!--p68-->
```java
int x = 96; // Illegal
}
}
```
```java
{
String s = new String("a string");
} // End of scope
```
```java
class ATypeName { /* Class body goes here */ }
```

<!--p69-->
```java
ATypeName a = new ATypeName();
```
```java
class DataOnly {
int i;
double d;
boolean b;
}
```
```java
DataOnly data = new DataOnly();
```
```java
objectReference.member
```
```java
data.i = 47;
data.d = 1.1;
data.b = false;
```
```java
myPlane.leftTank.capacity = 100;
```

<!--p70-->
```java
int x;
```
```java
ReturnType methodName( /* Argument list */ ) {
/* Method body */
}
```

<!--p71-->
```java
objectName.methodName(arg1, arg2, arg3);
```
```java
int x = a.f();
```
```java
int storage(String s) {
return s.length() * 2;
}
```
```java
boolean flag() { return true; }
double naturalLogBase() { return 2.718; }
void nothing() { return; }
void nothing2() {}
```

<!--p72-->

<!--p73-->
```java
import java.util.ArrayList;
```
```java
import java.util.*;
```
```java
class StaticTest {
static int i = 47;
}
```
```java
StaticTest st1 = new StaticTest();
StaticTest st2 = new StaticTest();
```

<!--p74-->
```java
StaticTest.i++;
```
```java
class Incrementable {
static void increment() { StaticTest.i++; }
}
```
```java
Incrementable sf = new Incrementable();
sf.increment();
```
```java
Incrementable.increment();
```

<!--p75-->
```java
// HelloDate.java
import java.util.*;
public class HelloDate {
public static void main(String[] args) {
System.out.println("Hello, it’s: ");
System.out.println(new Date());
}
}
```
```java
System.out.println("A String of things");
```
```java
public static void main(String[] args) {
```
```java
System.out.println(new Date());
```

<!--p76-->
```java
//: object/ShowProperties.java
public class ShowProperties {
public static void main(String[] args) {
System.getProperties().list(System.out);
System.out.println(System.getProperty("user.name"));
System.out.println(
System.getProperty("java.library.path"));
}
} ///:~
```
```java
javac HelloDate.java
```
```java
java HelloDate
```

<!--p77-->
```java
/* This is a comment
* that continues
* across lines
*/
```
```java
/* This is a comment that
continues across lines */
```
```java
// This is a one-line comment
```

<!--p78-->
```java
//: object/Documentation1.java
/** A class comment */
public class Documentation1 {
/** A field comment */
public int i;
/** A method comment */
public void f() {}
} ///:~
```
```java
//: object/Documentation2.java
/**
* <pre>
* System.out.println(new Date());
* </pre>
*/
///:~
```

<!--p79-->
```java
//: object/Documentation3.java
/**
* You can <em>even</em> insert a list:
* <ol>
* <li> Item one
* <li> Item two
* <li> Item three
* </ol>
*/
///:~
```
```java
@see classname
@see fully-qualified-classname
@see fully-qualified-classname#method-name
```

<!--p80-->
```java
@version version-information
```
```java
@author author-information
```
```java
@param parameter-name description
```
```java
@return description
```

<!--p81-->
```java
@throws fully-qualified-class-name description
```
```java
//: object/HelloDate.java
import java.util.*;
/** The first Thinking in Java example program.
* Displays a string and today’s date.
* @author Bruce Eckel
* @author www.MindView.net
* @version 4.0
*/
public class HelloDate {
/** Entry point to class & application.
* @param args array of string arguments
* @throws exceptions No exceptions thrown
*/
public static void main(String[] args) {
System.out.println("Hello, it’s: ");
System.out.println(new Date());
}
} /* Output: (55% match)
Hello, it’s:
Wed Oct 05 14:39:36 MDT 2005
*///:~
```

<!--p82-->
```java
class AllTheColorsOfTheRainbow { // ...
```
```java
class AllTheColorsOfTheRainbow {
int anIntegerRepresentingColors;
void changeTheHueOfTheColor(int newHue) {
// ...
}
// ...
}
```

<!--p83-->

<!--p84-->