# 6. Access Control (printed p145-164)


<!--p167-->

<!--p168-->
Access Control Access control (or implementation hiding) is about “not getting it right the first time.” All good writers—including those who write software—know that a piece of work isn’t good until it’s been rewritten, often many times. If you leave a piece of code in a drawer for a while and come back to it, you may see a much better way to do it. This is one of the prime motivations for refactoring, which rewrites working code in order to make it more readable, understandable, and thus maintainable.1 There is a tension, however, in this desire to change and improve your code. There are often consumers (client programmers) who rely on some aspect of your code staying the same. So you want to change it; they want it to stay the same. Thus a primary consideration in object- oriented design is to “separate the things that change from the things that stay the same.” This is particularly important for libraries. Consumers of that library must rely on the part they use, and know that they won’t need to rewrite code if a new version of the library comes out. On the flip side, the library creator must have the freedom to make modifications and improvements with the certainty that the client code won’t be affected by those changes. This can be achieved through convention. For example, the library programmer must agree not to remove existing methods when modifying a class in the library, since that would break the client programmer’s code. The reverse situation is thornier, however. In the case of a field, how can the library creator know which fields have been accessed by client programmers? This is also true with methods that are only part of the implementation of a class, and not meant to be used directly by the client programmer. What if the library creator wants to rip out an old implementation and put in a new one? Changing any of those members might break a client programmer’s code. Thus the library creator is in a strait jacket and can’t change anything. To solve this problem, Java provides access specifiers to allow the library creator to say what is available to the client programmer and what is not. The levels of access control from “most access” to “least access” are public, protected, package access (which has no keyword), and private. From the previous paragraph you might think that, as a library designer, you’ll want to keep everything as “private” as possible, and expose only the methods that you want the client programmer to use. This is exactly right, even though it’s often counterintuitive for people who program in other languages (especially C) and who are used to accessing everything without restriction. By the end of this chapter you should be convinced of the value of access control in Java. The concept of a library of components and the control over who can access the components of that library is not complete, however. There’s still the question of how the components are bundled together into a cohesive library unit. This is controlled with the package keyword in Java, and the access specifiers are affected by whether a class is in the same package or in a separate package. So to begin this chapter, you’ll learn how library components are placed into packages. Then you’ll be able to understand the complete meaning of the access specifiers. 1See Refactoring: Improving the Design of Existing Code, by Martin Fowler, et al. (Addison-Wesley, 1999). Occasionally someone will argue against refactoring, suggesting that code which works is perfectly good and it’s a waste of time to refactor it. The problem with this way of thinking is that the lion’s share of a project’s time and money is not in the initial writing of the code, but in maintaining it. Making code easier to understand translates into very significant dollars.
## package: the library unit
A package contains a group of classes, organized together under a single namespace. For example, there’s a utility library that’s part of the standard Java distribution, organized under the namespace java.util. One of the classes in java.util is called ArrayList. One way to use an ArrayList is to specify the full name java.util.ArrayList.
```java
//: access/FullQualification.java
public class FullQualification {
public static void main(String[] args) {
java.util.ArrayList list = new java.util.ArrayList();
}
} ///:~
```
This rapidly becomes tedious, so you’ll probably want to use the import keyword instead. If you want to import a single class, you can name that class in the import statement:
```java
//: access/SingleImport.java
import java.util.ArrayList;
public class SingleImport {
public static void main(String[] args) {
ArrayList list = new java.util.ArrayList();
}
} ///:~
```
Now you can use ArrayList with no qualification. However, none of the other classes in java.util are available. To import everything, you simply use the ‘*’ as you’ve been seeing in the rest of the examples in this book:
```java
import java.util.*;
```

<!--p169-->
The reason for all this importing is to provide a mechanism to manage namespaces. The names of all your class members are insulated from each other. A method f( ) inside a class A will not clash with an f( ) that has the same signature in class B. But what about the class names? Suppose you create a Stack class that is installed on a machine that already has a Stack class that’s written by someone else? This potential clashing of names is why it’s important to have complete control over the namespaces in Java, and to create a unique identifier combination for each class. Most of the examples thus far in this book have existed in a single file and have been designed for local use, so they haven’t bothered with package names. These examples have actually been in packages: the “unnamed” or default package. This is certainly an option, and for simplicity’s sake this approach will be used whenever possible throughout the rest of this book. However, if you’re planning to create libraries or programs that are friendly to other Java programs on the same machine, you must think about preventing class name clashes. When you create a source-code file for Java, it’s commonly called a compilation unit (sometimes a translation unit). Each compilation unit must have a name ending in .java, and inside the compilation unit there can be a public class that must have the same name as the file (including capitalization, but excluding the .java file name extension). There can be only one public class in each compilation unit; otherwise, the compiler will complain. If there are additional classes in that compilation unit, they are hidden from the world outside that package because they’re not public, and they comprise “support” classes for the main public class. Access Control Code organization When you compile a .java file, you get an output file for each class in the .java file. Each output file has the name of a class in the .java file, but with an extension of .class. Thus you can end up with quite a few .class files from a small number of .java files. If you’ve programmed with a compiled language, you might be used to the compiler spitting out an intermediate form (usually an “obj” file) that is then packaged together with others of its kind using a linker (to create an executable file) or a librarian (to create a library). That’s not how Java works. A working program is a bunch of .class files, which can be packaged and compressed into a Java ARchive (JAR) file (using Java’s jar archiver). The Java interpreter is responsible for finding, loading, and interpreting2 these files. A library is a group of these class files. Each source file usually has a public class and any number of non-public classes, so there’s one public component for each source file. If you want to say that all these components (each in its own separate .java and .class files) belong together, that’s where the package keyword comes in. If you use a package statement, it must appear as the first non-comment in the file. When you say:
```java
package access;
```
you’re stating that this compilation unit is part of a library named access. Put another way, you’re saying that the public class name within this compilation unit is under the umbrella of the name access, and anyone who wants to use that name must either fully specify the name or use the import keyword in combination with access, using the choices given previously. (Note that the convention for Java package names is to use all lowercase letters, even for intermediate words.) For example, suppose the name of the file is MyClass.java. This means there can be one and only one public class in that file, and the name of that class must be MyClass (including the capitalization):
```java
//: access/mypackage/MyClass.java
package access.mypackage;
public class MyClass {
// ...
} ///:~
```
Now, if someone wants to use MyClass or, for that matter, any of the other public classes in access, they must use the import keyword to make the name or names in access available. The alternative is to give the fully qualified name:
```java
//: access/QualifiedMyClass.java
public class QualifiedMyClass {
public static void main(String[] args) {
access.mypackage.MyClass m =
new access.mypackage.MyClass();
}
} ///:~
```

<!--p170-->
2There’s nothing in Java that forces the use of an interpreter. There exist native-code Java compilers that generate a single executable file. The import keyword can make this much cleaner:
```java
//: access/ImportedMyClass.java
import access.mypackage.*;
public class ImportedMyClass {
public static void main(String[] args) {
MyClass m = new MyClass();
}
} ///:~
```

<!--p171-->
It’s worth keeping in mind that what the package and import keywords allow you to do, as a library designer, is to divide up the single global namespace so you won’t have clashing names, no matter how many people get on the Internet and start writing classes in Java. Creating unique package names You might observe that, since a package never really gets “packaged” into a single file, a package can be made up of many .class files, and things could get a bit cluttered. To prevent this, a logical thing to do is to place all the .class files for a particular package into a single directory; that is, use the hierarchical file structure of the operating system to your advantage. This is one way that Java references the problem of clutter; you’ll see the other way later when the jar utility is introduced. Collecting the package files into a single subdirectory solves two other problems: creating unique package names, and finding those classes that might be buried in a directory structure someplace. This is accomplished by encoding the path of the location of the .class file into the name of the package. By convention, the first part of the package name is the reversed Internet domain name of the creator of the class. Since Internet domain names are guaranteed to be unique, if you follow this convention, your package name will be unique and you’ll never have a name clash. (That is, until you lose the domain name to someone else who starts writing Java code with the same path names as you did.) Of course, if you don’t have your own domain name, then you must fabricate an unlikely combination (such as your first and last name) to create unique package names. If you’ve decided to start publishing Java code, it’s worth the relatively small effort to get a domain name. The second part of this trick is resolving the package name into a directory on your machine, so that when the Java program runs and it needs to load the .class file, it can locate the directory where the .class file resides. The Java interpreter proceeds as follows. First, it finds the environment variable CLASSPATH3 (set via the operating system, and sometimes by the installation program that installs Java or a Java-based tool on your machine). CLASSPATH contains one or more directories that are used as roots in a search for .class files. Starting at that root, the interpreter will take the package name and replace each dot with a slash to generate a path name off of the CLASSPATH root (so package foo.bar.baz becomes foo\bar\baz or foo/bar/baz or possibly something else, depending on your operating system). This is then concatenated to the various entries in the CLASSPATH. That’s where it looks for the .class file with the name corresponding to the class you’re trying to create. (It also searches some standard directories relative to where the Java interpreter resides.) To understand this, consider my domain name, which is MindView.net. By reversing this and making it all lowercase, net.mindview establishes my unique global name for my classes. (The com, edu, org, etc., extensions were formerly capitalized in Java packages, but this was changed in Java 2 so the entire package name is lowercase.) I can further subdivide 3When referring to the environment variable, capital letters will be used (CLASSPATH). this by deciding that I want to create a library named simple, so I’ll end up with a package name:
```java
package net.mindview.simple;
```
Now this package name can be used as an umbrella namespace for the following two files:
```java
//: net/mindview/simple/Vector.java
// Creating a package.
package net.mindview.simple;
public class Vector {
public Vector() {
System.out.println("net.mindview.simple.Vector");
}
} ///:~
```
As mentioned before, the package statement must be the first non-comment code in the file. The second file looks much the same:
```java
//: net/mindview/simple/List.java
// Creating a package.
package net.mindview.simple;
public class List {
public List() {
System.out.println("net.mindview.simple.List");
}
} ///:~
```
Both of these files are placed in the subdirectory on my system:
```java
C:\DOC\JavaT\net\mindview\simple
```
(Notice that the first comment line in every file in this book establishes the directory location of that file in the source-code tree—this is used by the automatic code-extraction tool for this book.) If you walk back through this path, you can see the package name net.mindview.simple, but what about the first portion of the path? That’s taken care of by the CLASSPATH environment variable, which is, on my machine:
```java
CLASSPATH=.;D:\JAVA\LIB;C:\DOC\JavaT
```
You can see that the CLASSPATH can contain a number of alternative search paths. There’s a variation when using JAR files, however. You must put the actual name of the JAR file in the classpath, not just the path where it’s located. So for a JAR named grape.jar your classpath would include:
```java
CLASSPATH=.;D:\JAVA\LIB;C:\flavors\grape.jar
```
Once the classpath is set up properly, the following file can be placed in any directory:
```java
//: access/LibTest.java
// Uses the library.
import net.mindview.simple.*;
```

<!--p172-->
Access Control
```java
public class LibTest {
public static void main(String[] args) {
Vector v = new Vector();
List l = new List();
}
} /* Output:
net.mindview.simple.Vector
net.mindview.simple.List
*///:~
```
When the compiler encounters the import statement for the simple library, it begins searching at the directories specified by CLASSPATH, looking for subdirectory net/mindview/simple, then seeking the compiled files of the appropriate names (Vector.class for Vector, and List.class for List). Note that both the classes and the desired methods in Vector and List must be public. Setting the CLASSPATH has been such a trial for beginning Java users (it was for me, when I started) that Sun made the JDK in later versions of Java a bit smarter. You’ll find that when you install it, even if you don’t set the CLASSPATH, you’ll be able to compile and run basic Java programs. To compile and run the source-code package for this book (available at www.MindView.net), however, you will need to add the base directory of the book’s code tree to your CLASSPATH. Exercise 1:(1) Create a class in a package. Create an instance of your class outside of that package. Collisions What happens if two libraries are imported via ‘*’ and they include the same names? For example, suppose a program does this:
```java
import net.mindview.simple.*;
import java.util.*;
```
Since java.util.* also contains a Vector class, this causes a potential collision. However, as long as you don’t write the code that actually causes the collision, everything is OK—this is good, because otherwise you might end up doing a lot of typing to prevent collisions that would never happen. The collision does occur if you now try to make a Vector:
```java
Vector v = new Vector();
```
Which Vector class does this refer to? The compiler can’t know, and the reader can’t know either. So the compiler complains and forces you to be explicit. If I want the standard Java Vector, for example, I must say:
```java
java.util.Vector v = new java.util.Vector();
```

<!--p173-->
Since this (along with the CLASSPATH) completely specifies the location of that Vector, there’s no need for the import java.util.* statement unless I’m using something else from java.util. Alternatively, you can use the single-class import form to prevent clashes—as long as you don’t use both colliding names in the same program (in which case you must fall back to fully specifying the names). Exercise 2:(1) Take the code fragments in this section and turn them into a program, and verify that collisions do in fact occur. A custom tool library With this knowledge, you can now create your own libraries of tools to reduce or eliminate duplicate code. Consider, for example, the alias we’ve been using for System.out.println( ), to reduce typing. This can be part of a class called Print so that you end up with a readable static import:
```java
//: net/mindview/util/Print.java
// Print methods that can be used without
// qualifiers, using Java SE5 static imports:
package net.mindview.util;
import java.io.*;
public class Print {
// Print with a newline:
public static void print(Object obj) {
System.out.println(obj);
}
// Print a newline by itself:
public static void print() {
System.out.println();
}
// Print with no line break:
public static void printnb(Object obj) {
System.out.print(obj);
}
// The new Java SE5 printf() (from C):
public static PrintStream
printf(String format, Object... args) {
return System.out.printf(format, args);
}
} ///:~
```
You can use the printing shorthand to print anything, either with a newline (print( )) or without a newline (printnb( )). You can guess that the location of this file must be in a directory that starts at one of the CLASSPATH locations, then continues into net/mindview. After compiling, the static print( ) and printnb( ) methods can be used anywhere on your system with an import static statement:
```java
//: access/PrintTest.java
// Uses the static printing methods in Print.java.
import static net.mindview.util.Print.*;
public class PrintTest {
public static void main(String[] args) {
print("Available from now on!");
print(100);
print(100L);
print(3.14159);
}
} /* Output:
Available from now on!
3.14159
```

<!--p174-->
Access Control
```java
*///:~
```
A second component of this library can be the range( ) methods, introduced in the Controlling Execution chapter, that allow the use of the foreach syntax for simple integer sequences:
```java
//: net/mindview/util/Range.java
// Array creation methods that can be used without
// qualifiers, using Java SE5 static imports:
package net.mindview.util;
public class Range {
// Produce a sequence [0..n)
public static int[] range(int n) {
int[] result = new int[n];
for(int i = 0; i < n; i++)
result[i] = i;
return result;
}
// Produce a sequence [start..end)
public static int[] range(int start, int end) {
int sz = end - start;
int[] result = new int[sz];
for(int i = 0; i < sz; i++)
result[i] = start + i;
return result;
}
// Produce a sequence [start..end) incrementing by step
public static int[] range(int start, int end, int step) {
int sz = (end - start)/step;
int[] result = new int[sz];
for(int i = 0; i < sz; i++)
result[i] = start + (i * step);
return result;
}
} ///:~
```

<!--p175-->

<!--p176-->
From now on, whenever you come up with a useful new utility, you can add it to your own library. You’ll see more components added to the net.mindview.util library throughout the book. Using imports to change behavior A feature that is missing from Java is C’s conditional compilation, which allows you to change a switch and get different behavior without changing any other code. The reason such a feature was left out of Java is probably because it is most often used in C to solve cross- platform issues: Different portions of the code are compiled depending on the target platform. Since Java is intended to be automatically cross-platform, such a feature should not be necessary. However, there are other valuable uses for conditional compilation. A very common use is for debugging code. The debugging features are enabled during development and disabled in the shipping product. You can accomplish this by changing the package that’s imported in order to change the code used in your program from the debug version to the production version. This technique can be used for any kind of conditional code. Exercise 3:(2) Create two packages: debug and debugoff, containing an identical class with a debug( ) method. The first version displays its String argument to the console, the second does nothing. Use a static import line to import the class into a test program, and demonstrate the conditional compilation effect. Package caveat It’s worth remembering that anytime you create a package, you implicitly specify a directory structure when you give the package a name. The package must live in the directory indicated by its name, which must be a directory that is searchable starting from the CLASSPATH. Experimenting with the package keyword can be a bit frustrating at first, because unless you adhere to the package-name to directory-path rule, you’ll get a lot of mysterious runtime messages about not being able to find a particular class, even if that class is sitting there in the same directory. If you get a message like this, try commenting out the package statement, and if it runs, you’ll know where the problem lies. Note that compiled code is often placed in a different directory than source code, but the path to the compiled code must still be found by the JVM using the CLASSPATH. Java access specifiers The Java access specifiers public, protected, and private are placed in front of each definition for each member in your class, whether it’s a field or a method. Each access specifier only controls the access for that particular definition. If you don’t provide an access specifier, it means “package access.” So one way or another, everything has some kind of access control. In the following sections, you’ll learn about the various types of access. Package access All the examples before this chapter used no access specifiers. The default access has no keyword, but it is commonly referred to as package access (and sometimes “friendly”). It means that all the other classes in the current package have access to that member, but to all the classes outside of this package, the member appears to be private. Since a compilation unit—a file—can belong only to a single package, all the classes within a single compilation unit are automatically available to each other via package access. Package access allows you to group related classes together in a package so that they can easily interact with each other. When you put classes together in a package, thus granting mutual access to their package-access members, you “own” the code in that package. It makes sense that only code that you own should have package access to other code that you own. You could say that package access gives a meaning or a reason for grouping classes together in a package. In many languages the way you organize your definitions in files can be arbitrary, but in Java you’re compelled to organize them in a sensible fashion. In addition, you’ll probably want to exclude classes that shouldn’t have access to the classes being defined in the current package. The class controls the code that has access to its members. Code from another package can’t just come around and say, “Hi, I’m a friend of Bob’s!” and expect to be shown the protected, package-access, and private members of Bob. The only way to grant access to a member is to: 1.Make the member public. Then everybody, everywhere, can access it. Access Control 2.Give the member package access by leaving off any access specifier, and put the other classes in the same package. Then the other classes in that package can access the member. 3.As you’ll see in the Reusing Classes chapter, when inheritance is introduced, an inherited class can access a protected member as well as a public member (but not private members). It can access package-access members only if the two classes are in the same package. But don’t worry about inheritance and protected right now. 4.Provide “accessor/mutator” methods (also known as “get/set” methods) that read and change the value. This is the most civilized approach in terms of OOP, and it is fundamental to JavaBeans, as you’ll see in the Graphical User Interfaces chapter.
## public: interface access
When you use the public keyword, it means that the member declaration that immediately follows public is available to everyone, in particular to the client programmer who uses the library. Suppose you define a package dessert containing the following compilation unit:
```java
//: access/dessert/Cookie.java
// Creates a library.
package access.dessert;
public class Cookie {
public Cookie() {
System.out.println("Cookie constructor");
}
void bite() { System.out.println("bite"); }
} ///:~
```
Remember, the class file produced by Cookie.java must reside in a subdirectory called dessert, in a directory under access (indicating the Access Control chapter of this book) that must be under one of the CLASSPATH directories. Don’t make the mistake of thinking that Java will always look at the current directory as one of the starting points for searching. If you don’t have a ‘.’ as one of the paths in your CLASSPATH, Java won’t look there. Now if you create a program that uses Cookie:
```java
//: access/Dinner.java
// Uses the library.
import access.dessert.*;
public class Dinner {
public static void main(String[] args) {
Cookie x = new Cookie();
//! x.bite(); // Can’t access
}
} /* Output:
Cookie constructor
*///:~
```

<!--p177-->
you can create a Cookie object, since its constructor is public and the class is public. (We’ll look more at the concept of a public class later.) However, the bite( ) member is inaccessible inside Dinner.java since bite( ) provides access only within package dessert, so the compiler prevents you from using it. The default package You might be surprised to discover that the following code compiles, even though it would appear that it breaks the rules:
```java
//: access/Cake.java
// Accesses a class in a separate compilation unit.
class Cake {
public static void main(String[] args) {
Pie x = new Pie();
x.f();
}
} /* Output:
Pie.f()
*///:~
```
In a second file in the same directory:
```java
//: access/Pie.java
// The other class.
class Pie {
void f() { System.out.println("Pie.f()"); }
} ///:~
```
You might initially view these as completely foreign files, and yet Cake is able to create a Pie object and call its f( ) method. (Note that you must have ‘.’ in your CLASSPATH in order for the files to compile.) You’d typically think that Pie and f( ) have package access and are therefore not available to Cake. They do have package access—that part is correct. The reason that they are available in Cake.java is because they are in the same directory and have no explicit package name. Java treats files like this as implicitly part of the “default package” for that directory, and thus they provide package access to all the other files in that directory.
## private: you can’t touch that!
The private keyword means that no one can access that member except the class that contains that member, inside methods of that class. Other classes in the same package cannot access private members, so it’s as if you’re even insulating the class against yourself. On the other hand, it’s not unlikely that a package might be created by several people collaborating together, so private allows you to freely change that member without concern that it will affect another class in the same package. The default package access often provides an adequate amount of hiding; remember, a packageaccess member is inaccessible to the client programmer using the class. This is nice, since the default access is the one that you normally use (and the one that you’ll get if you forget to add any access control). Thus, you’ll typically think about access for the members that you explicitly want to make public for the client programmer, and as a result, you might initially think that you won’t use the private keyword very often, since it’s tolerable to get away without it. However, it turns out that the consistent use of private is very important, especially where multithreading is concerned. (As you’ll see in the Concurrency chapter.) Here’s an example of the use of private:
```java
//: access/IceCream.java
// Demonstrates "private" keyword.
```

<!--p178-->
Access Control
```java
class Sundae {
private Sundae() {}
static Sundae makeASundae() {
return new Sundae();
}
}
public class IceCream {
public static void main(String[] args) {
//! Sundae x = new Sundae();
Sundae x = Sundae.makeASundae();
}
} ///:~
```
This shows an example in which private comes in handy: You might want to control how an object is created and prevent someone from directly accessing a particular constructor (or all of them). In the preceding example, you cannot create a Sundae object via its constructor; instead, you must call the makeASundae( ) method to do it for you.4 Any method that you’re certain is only a “helper” method for that class can be made private, to ensure that you don’t accidentally use it elsewhere in the package and thus prohibit yourself from changing or removing the method. Making a method private guarantees that you retain this option. The same is true for a private field inside a class. Unless you must expose the underlying implementation (which is less likely than you might think), you should make all fields private. However, just because a reference to an object is private inside a class doesn’t mean that some other object can’t have a public reference to the same object. (See the online supplements for this book to learn about aliasing issues.)
## protected: inheritance access
Understanding the protected access specifier requires a jump ahead. First, you should be aware that you don’t need to understand this section to continue through this book up through inheritance (the Reusing Classes chapter). But for completeness, here is a brief description and example using protected. The protected keyword deals with a concept called inheritance, which takes an existing class— which we refer to as the base class—and adds new members to that class without touching the existing class. You can also change the behavior of existing members of the class. To inherit from a class, you say that your new class extends an existing class, like this:
```java
class Foo extends Bar {
```

<!--p179-->
The rest of the class definition looks the same. If you create a new package and inherit from a class in another package, the only members you have access to are the public members of the original package. (Of course, if you perform the inheritance in the same package, you can manipulate all the members that have package access.) Sometimes the creator of the base class would like to take a particular member and grant access to derived classes but not the world in general. That’s what protected does. protected also gives package access—that is, other classes in the same package may access protected elements. 4There’s another effect in this case: Since the default constructor is the only one defined, and it’s private, it will prevent inheritance of this class. (A subject that will be introduced later.) If you refer back to the file Cookie.java, the following class cannot call the package-access member bite( ):
```java
//: access/ChocolateChip.java
// Can’t use package-access member from another package.
import access.dessert.*;
public class ChocolateChip extends Cookie {
public ChocolateChip() {
System.out.println("ChocolateChip constructor");
}
public void chomp() {
//! bite(); // Can’t access bite
}
public static void main(String[] args) {
ChocolateChip x = new ChocolateChip();
x.chomp();
}
} /* Output:
Cookie constructor
ChocolateChip constructor
*///:~
```
One of the interesting things about inheritance is that if a method bite( ) exists in class Cookie, then it also exists in any class inherited from Cookie. But since bite( ) has package access and is in a foreign package, it’s unavailable to us in this one. Of course, you could make it public, but then everyone would have access, and maybe that’s not what you want. If you change the class Cookie as follows:
```java
//: access/cookie2/Cookie.java
package access.cookie2;
public class Cookie {
public Cookie() {
System.out.println("Cookie constructor");
}
protected void bite() {
System.out.println("bite");
}
} ///:~
```
now bite( ) becomes accessible to anyone inheriting from Cookie:
```java
//: access/ChocolateChip2.java
import access.cookie2.*;
public class ChocolateChip2 extends Cookie {
public ChocolateChip2() {
System.out.println("ChocolateChip2 constructor");
}
public void chomp() { bite(); } // Protected method
public static void main(String[] args) {
ChocolateChip2 x = new ChocolateChip2();
x.chomp();
}
} /* Output:
Cookie constructor
ChocolateChip2 constructor
bite
*///:~
```

<!--p180-->
Access Control Note that, although bite( ) also has package access, it is not public. Exercise 4:(2) Show that protected methods have package access but are not public. Exercise 5:(2) Create a class with public, private, protected, and package-access fields and method members. Create an object of this class and see what kind of compiler messages you get when you try to access all the class members. Be aware that classes in the same directory are part of the “default” package. Exercise 6:(1) Create a class with protected data. Create a second class in the same file with a method that manipulates the protected data in the first class. Interface and implementation Access control is often referred to as implementation hiding. Wrapping data and methods within classes in combination with implementation hiding is often called encapsulation.5 The result is a data type with characteristics and behaviors. Access control puts boundaries within a data type for two important reasons. The first is to establish what the client programmers can and can’t use. You can build your internal mechanisms into the structure without worrying that the client programmers will accidentally treat the internals as part of the interface that they should be using. This feeds directly into the second reason, which is to separate the interface from the implementation. If the structure is used in a set of programs, but client programmers can’t do anything but send messages to the public interface, then you are free to change anything that’s not public (e.g., package access, protected, or private) without breaking client code. For clarity, you might prefer a style of creating classes that puts the public members at the beginning, followed by the protected, package-access, and private members. The advantage is that the user of the class can then read down from the top and see first what’s important to them (the public members, because they can be accessed outside the file), and stop reading when they encounter the non-public members, which are part of the internal implementation:
```java
//: access/OrganizedByAccess.java
public class OrganizedByAccess {
public void pub1() { /* ... */ }
public void pub2() { /* ... */ }
public void pub3() { /* ... */ }
private void priv1() { /* ... */ }
private void priv2() { /* ... */ }
private void priv3() { /* ... */ }
private int i;
// ...
} ///:~
```

<!--p181-->
This will make it only partially easier to read, because the interface and implementation are still mixed together. That is, you still see the source code—the implementation—because it’s right there in the class. In addition, the comment documentation supported by Javadoc lessens the importance of code readability by the client programmer. Displaying the interface to the consumer of a class is really the job of the class browser, a tool whose job is to look at all the available classes and show you what you can do with them (i.e., what members are 5However, people often refer to implementation hiding alone as encapsulation. available) in a useful fashion. In Java, viewing the JDK documentation with a Web browser gives you the same effect as a class browser. Class access In Java, the access specifiers can also be used to determine which classes within a library will be available to the users of that library. If you want a class to be available to a client programmer, you use the public keyword on the entire class definition. This controls whether the client programmer can even create an object of the class. To control the access of a class, the specifier must appear before the keyword class. Thus you can say:
```java
public class Widget {
```
Now if the name of your library is access, any client programmer can access Widget by saying
```java
import access.Widget;
```
or
```java
import access.*;
```

<!--p182-->
However, there’s an extra set of constraints: 1.There can be only one public class per compilation unit (file). The idea is that each compilation unit has a single public interface represented by that public class. It can have as many supporting package-access classes as you want. If you have more than one public class inside a compilation unit, the compiler will give you an error message. 2.The name of the public class must exactly match the name of the file containing the compilation unit, including capitalization. So for Widget, the name of the file must be Widget.java, not widget.java or WIDGET.java. Again, you’ll get a compile-time error if they don’t agree. 3.It is possible, though not typical, to have a compilation unit with no public class at all. In this case, you can name the file whatever you like (although naming it arbitrarily will be confusing to people reading and maintaining the code). What if you’ve got a class inside access that you’re only using to accomplish the tasks performed by Widget or some other public class in access? You don’t want to go to the bother of creating documentation for the client programmer, and you think that sometime later you might want to completely change things and rip out your class altogether, substituting a different one. To give you this flexibility, you need to ensure that no client programmers become dependent on your particular implementation details hidden inside access. To accomplish this, you just leave the public keyword off the class, in which case it has package access. (That class can be used only within that package.) Exercise 7:(1) Create the library according to the code fragments describing access and Widget. Create a Widget in a class that is not part of the access package. When you create a package-access class, it still makes sense to make the fields of the class private—you should always make fields as private as possible—but it’s generally reasonable to give the methods the same access as the class (package access). Since a package-access Access Control class is usually used only within the package, you only need to make the methods of such a class public if you’re forced to, and in those cases, the compiler will tell you. Note that a class cannot be private (that would make it inaccessible to anyone but the class) or protected.6 So you have only two choices for class access: package access or public. If you don’t want anyone else to have access to that class, you can make all the constructors private, thereby preventing anyone but you, inside a static member of the class, from creating an object of that class. Here’s an example:
```java
//: access/Lunch.java
// Demonstrates class access specifiers. Make a class
// effectively private with private constructors:
class Soup1 {
private Soup1() {}
// (1) Allow creation via static method:
public static Soup1 makeSoup() {
return new Soup1();
}
}
class Soup2 {
private Soup2() {}
// (2) Create a static object and return a reference
// upon request.(The "Singleton" pattern):
private static Soup2 ps1 = new Soup2();
public static Soup2 access() {
return ps1;
}
public void f() {}
}
// Only one public class allowed per file:
public class Lunch {
void testPrivate() {
// Can’t do this! Private constructor:
//! Soup1 soup = new Soup1();
}
void testStatic() {
Soup1 soup = Soup1.makeSoup();
}
void testSingleton() {
Soup2.access().f();
}
} ///:~
```
Up to now, most of the methods have been returning either void or a primitive type, so the definition:
```java
public static Soup1 makeSoup() {
return new Soup1();
}
```

<!--p183-->
might look a little confusing at first. The word Soup1 before the method name (makeSoup) tells what the method returns. So far in this book, this has usually been void, which means it returns nothing. But you can also return a reference to an object, which is what happens here. This method returns a reference to an object of class Soup1. 6Actually, an inner class can be private or protected, but that’s a special case. These will be introduced in the Inner Classes chapter. The classes Soup1 and Soup2 show how to prevent direct creation of a class by making all the constructors private. Remember that if you don’t explicitly create at least one constructor, the default constructor (a constructor with no arguments) will be created for you. By writing the default constructor, it won’t be created automatically. By making it private, no one can create an object of that class. But now how does anyone use this class? The preceding example shows two options. In Soup1, a static method is created that creates a new Soup1 and returns a reference to it. This can be useful if you want to do some extra operations on the Soup1 before returning it, or if you want to keep count of how many Soup1 objects to create (perhaps to restrict their population). Soup2 uses what’s called a design pattern, which is covered in Thinking in Patterns (with Java) at www.MindView.net. This particular pattern is called a Singleton, because it allows only a single object to ever be created. The object of class Soup2 is created as a static private member of Soup2, so there’s one and only one, and you can’t get at it except through the public method access( ). As previously mentioned, if you don’t put an access specifier for class access, it defaults to package access. This means that an object of that class can be created by any other class in the package, but not outside the package. (Remember, all the files within the same directory that don’t have explicit package declarations are implicitly part of the default package for that directory.) However, if a static member of that class is public, the client programmer can still access that static member even though they cannot create an object of that class. Exercise 8:(4) Following the form of the example Lunch.java, create a class called ConnectionManager that manages a fixed array of Connection objects. The client programmer must not be able to explicitly create Connection objects, but can only get them via a static method in ConnectionManager. When the ConnectionManager runs out of objects, it returns a null reference. Test the classes in main( ). Exercise 9:(2) Create the following file in the access/local directory (presumably in your CLASSPATH):
```java
// access/local/PackagedClass.java
package access.local;
class PackagedClass {
public PackagedClass() {
System.out.println("Creating a packaged class");
}
}
```
Then create the following file in a directory other than access/local:
```java
// access/foreign/Foreign.java
package access.foreign;
import access.local.*;
public class Foreign {
public static void main(String[] args) {
PackagedClass pc = new PackagedClass();
}
}
```

<!--p184-->

<!--p185-->
Explain why the compiler generates an error. Would making the Foreign class part of the access.local package change anything? Access Control Summary In any relationship it’s important to have boundaries that are respected by all parties involved. When you create a library, you establish a relationship with the user of that library—the client programmer—who is another programmer, but one using your library to build an application or a bigger library. Without rules, client programmers can do anything they want with all the members of a class, even if you might prefer they don’t directly manipulate some of the members. Everything’s naked to the world. This chapter looked at how classes are built to form libraries: first, the way a group of classes is packaged within a library, and second, the way the class controls access to its members. It is estimated that a C programming project begins to break down somewhere between 50K and 100K lines of code because C has a single namespace, and names begin to collide, causing extra management overhead. In Java, the package keyword, the package naming scheme, and the import keyword give you complete control over names, so the issue of name collision is easily avoided. There are two reasons for controlling access to members. The first is to keep users’ hands off portions that they shouldn’t touch. These pieces are necessary for the internal operations of the class, but not part of the interface that the client programmer needs. So making methods and fields private is a service to client programmers, because they can easily see what’s important to them and what they can ignore. It simplifies their understanding of the class. The second and most important reason for access control is to allow the library designer to change the internal workings of the class without worrying about how it will affect the client programmer. You might, for example, build a class one way at first, and then discover that restructuring your code will provide much greater speed. If the interface and implementation are clearly separated and protected, you can accomplish this without forcing client programmers to rewrite their code. Access control ensures that no client programmer becomes dependent on any part of the underlying implementation of a class. When you have the ability to change the underlying implementation, you not only have the freedom to improve your design, you also have the freedom to make mistakes. No matter how carefully you plan and design, you’ll make mistakes. Knowing that it’s relatively safe to make these mistakes means you’ll be more experimental, you’ll learn more quickly, and you’ll finish your project sooner. The public interface to a class is what the user does see, so that is the most important part of the class to get “right” during analysis and design. Even that allows you some leeway for change. If you don’t get the interface right the first time, you can add more methods, as long as you don’t remove any that client programmers have already used in their code. Notice that access control focuses on a relationship—and a kind of communication—between a library creator and the external clients of that library. There are many situations where this is not the case. For example, you are writing all the code yourself, or you are working in close quarters with a small team and everything goes into the same package. These situations have a different kind of communication, and rigid adherence to access rules may not be optimal. Default (package) access may be just fine. Access Control Solutions to selected exercises can be found in the electronic document The Thinking in Java Annotated Solution Guide, available for sale from www.MindView.net.