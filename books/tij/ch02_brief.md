# 2. Everything Is an Object (printed p41-62)


<!--p63-->

<!--p64-->
Everything Is an Object “If we spoke a different language, we would perceive a somewhat different world.” Ludwig Wittgenstein (1889-1951) Although it is based on C++, Java is more of a “pure” object-oriented language. Both C++ and Java are hybrid languages, but in Java the designers felt that the hybridization was not as important as it was in C++. A hybrid language allows multiple programming styles; the reason C++ is hybrid is to support backward compatibility with the C language. Because C++ is a superset of the C language, it includes many of that language’s undesirable features, which can make some aspects of C++ overly complicated. The Java language assumes that you want to do only object-oriented programming. This means that before you can begin you must shift your mindset into an object-oriented world (unless it’s already there). The benefit of this initial effort is the ability to program in a language that is simpler to learn and to use than many other OOP languages. In this chapter you’ll see the basic components of a Java program and learn that (almost) everything in Java is an object. You manipulate objects with references Each programming language has its own means of manipulating elements in memory. Sometimes the programmer must be constantly aware of what type of manipulation is going on. Are you manipulating the element directly, or are you dealing with some kind of indirect representation (a pointer in C or C++) that must be treated with a special syntax? All this is simplified in Java. You treat everything as an object, using a single consistent syntax. Although you treat everything as an object, the identifier you manipulate is actually a “reference” to an object.1 You might imagine a television (the object) and a remote control (the reference). As long as you’re holding this reference, you have a connection to the television, but when someone says, “Change the channel” or “Lower the volume,” what you’re manipulating is the reference, which in turn modifies the object. If you want to move around 1 This can be a flashpoint. There are those who say, “Clearly, it’s a pointer,” but this presumes an underlying implementation. Also, Java references are much more akin to C++ references than to pointers in their syntax. In the 1st edition of this book, I chose to invent a new term, “handle,” because C++ references and Java references have some important differences. I was coming out of C++ and did not want to confuse the C++ programmers whom I assumed would be the largest audience for Java. In the 2nd edition, I decided that “reference” was the more commonly used term, and that anyone changing from C++ would have a lot more to cope with than the terminology of references, so they might as well jump in with both feet. However, there are people who disagree even with the term “reference.” I read in one book where it was “completely wrong to say that Java supports pass by reference,” because Java object identifiers (according to that author) are actually “object references.” And (he goes on) everything is actually pass by value. So you’re not passing by reference, you’re “passing an object reference by value.” One could argue for the precision of such convoluted explanations, but I think my approach simplifies the understanding of the concept without hurting anything (well, the language lawyers may claim that I’m lying to you, but I’ll say that I’m providing an appropriate abstraction). the room and still control the television, you take the remote/reference with you, not the television. Also, the remote control can stand on its own, with no television. That is, just because you have a reference doesn’t mean there’s necessarily an object connected to it. So if you want to hold a word or sentence, you create a String reference:
```java
String s;
```
But here you’ve created only the reference, not an object. If you decided to send a message to s at this point, you’ll get an error because s isn’t actually attached to anything (there’s no television). A safer practice, then, is always to initialize a reference when you create it:
```java
String s = "asdf";
```
However, this uses a special Java feature: Strings can be initialized with quoted text. Normally, you must use a more general type of initialization for objects. You must create all the objects When you create a reference, you want to connect it with a new object. You do so, in general, with the new operator. The keyword new says, “Make me a new one of these objects.” So in the preceding example, you can say:
```java
String s = new String("asdf");
```

<!--p65-->

<!--p66-->
Not only does this mean “Make me a new String,” but it also gives information about how to make the String by supplying an initial character string. Of course, Java comes with a plethora of ready-made types in addition to String. What’s more important is that you can create your own types. In fact, creating new types is the fundamental activity in Java programming, and it’s what you’ll be learning about in the rest of this book. Where storage lives It’s useful to visualize some aspects of how things are laid out while the program is running— in particular how memory is arranged. There are five different places to store data: 1.Registers. This is the fastest storage because it exists in a place different from that of other storage: inside the processor. However, the number of registers is severely limited, so registers are allocated as they are needed. You don’t have direct control, nor do you see any evidence in your programs that registers even exist (C & C++, on the other hand, allow you to suggest register allocation to the compiler). 2.The stack. This lives in the general random-access memory (RAM) area, but has direct support from the processor via its stack pointer. The stack pointer is moved down to create new memory and moved up to release that memory. This is an extremely fast and efficient way to allocate storage, second only to registers. The Java system must know, while it is creating the program, the exact lifetime of all the items that are stored on the stack. This constraint places limits on the flexibility of your programs, so while some Java storage exists on the stack—in particular, object references—Java objects themselves are not placed on the stack. Everything Is an Object 3.The heap. This is a general-purpose pool of memory (also in the RAM area) where all Java objects live. The nice thing about the heap is that, unlike the stack, the compiler doesn’t need to know how long that storage must stay on the heap. Thus, there’s a great deal of flexibility in using storage on the heap. Whenever you need an object, you simply write the code to create it by using new, and the storage is allocated on the heap when that code is executed. Of course there’s a price you pay for this flexibility: It may take more time to allocate and clean up heap storage than stack storage (if you even could create objects on the stack in Java, as you can in C++). 4.Constant storage. Constant values are often placed directly in the program code, which is safe since they can never change. Sometimes constants are cordoned off by themselves so that they can be optionally placed in read-only memory (ROM), in embedded systems.2 5.Non-RAM storage. If data lives completely outside a program, it can exist while the program is not running, outside the control of the program. The two primary examples of this are streamed objects, in which objects are turned into streams of bytes, generally to be sent to another machine, and persistent objects, in which the objects are placed on disk so they will hold their state even when the program is terminated. The trick with these types of storage is turning the objects into something that can exist on the other medium, and yet can be resurrected into a regular RAM- based object when necessary. Java provides support for lightweight persistence, and mechanisms such as JDBC and Hibernate provide more sophisticated support for storing and retrieving object information in databases. Special case: primitive types One group of types, which you’ll use quite often in your programming, gets special treatment. You can think of these as “primitive” types. The reason for the special treatment is that to create an object with new—especially a small, simple variable—isn’t very efficient, because new places objects on the heap. For these types Java falls back on the approach taken by C and C++. That is, instead of creating the variable by using new, an “automatic” variable is created that is not a reference. The variable holds the value directly, and it’s placed on the stack, so it’s much more efficient. Java determines the size of each primitive type. These sizes don’t change from one machine architecture to another as they do in most languages. This size invariance is one reason Java programs are more portable than programs in most other languages. Primitive type Size Minimum Maximum Wrapper type boolean — — — Boolean char 16 bits Unicode 0 Unicode 216- 1 Character byte 8 bits -128 +127 Byte short 16 bits -215 +215-1 Short int 32 bits -231 +231-1 Integer long 64 bits -263 +263-1 Long float 32 bits IEEE754 IEEE754 Float double 64 bits IEEE754 IEEE754 Double void — — — Void 2An example of this is the string pool. All literal strings and string-valued constant expressions are interned automatically and put into special static storage. All numeric types are signed, so don’t look for unsigned types. The size of the boolean type is not explicitly specified; it is only defined to be able to take the literal values true or false. The “wrapper” classes for the primitive data types allow you to make a non-primitive object on the heap to represent that primitive type. For example:
```java
char c = ‘x’;
Character ch = new Character(c);
```
Or you could also use:
```java
Character ch = new Character(‘x’);
```
Java SE5 autoboxing will automatically convert from a primitive to a wrapper type:
```java
Character ch = ‘x’;
```
and back:
```java
char c = ch;
```

<!--p67-->
The reasons for wrapping primitives will be shown in a later chapter. High-precision numbers Java includes two classes for performing high-precision arithmetic: BigInteger and BigDecimal. Although these approximately fit into the same category as the “wrapper” classes, neither one has a primitive analogue. Both classes have methods that provide analogues for the operations that you perform on primitive types. That is, you can do anything with a BigInteger or BigDecimal that you can with an int or float, it’s just that you must use method calls instead of operators. Also, since there’s more involved, the operations will be slower. You’re exchanging speed for accuracy. BigInteger supports arbitrary-precision integers. This means that you can accurately represent integral values of any size without losing any information during operations. BigDecimal is for arbitrary-precision fixed-point numbers; you can use these for accurate monetary calculations, for example. Consult the JDK documentation for details about the constructors and methods you can call for these two classes. Arrays in Java Virtually all programming languages support some kind of arrays. Using arrays in C and C++ is perilous because those arrays are only blocks of memory. If a program accesses the array outside of its memory block or uses the memory before initialization (common programming errors), there will be unpredictable results. One of the primary goals of Java is safety, so many of the problems that plague programmers in C and C++ are not repeated in Java. A Java array is guaranteed to be initialized and cannot be accessed outside of its range. The range checking comes at the price of having a small amount of memory overhead on each array as well as verifying the index at run time, but the assumption is that the safety and increased productivity are worth the expense (and Java can sometimes optimize these operations). When you create an array of objects, you are really creating an array of references, and each of those references is automatically initialized to a special value with its own keyword: null. When Java sees null, it recognizes that the reference in question isn’t pointing to an object. You must assign an object to each reference before you use it, and if you try to use a reference that’s still null, the problem will be reported at run time. Thus, typical array errors are prevented in Java. You can also create an array of primitives. Again, the compiler guarantees initialization because it zeroes the memory for that array. Arrays will be covered in detail in later chapters. You never need to destroy an object In most programming languages, the concept of the lifetime of a variable occupies a significant portion of the programming effort. How long does the variable last? If you are supposed to destroy it, when should you? Confusion over variable lifetimes can lead to a lot of bugs, and this section shows how Java greatly simplifies the issue by doing all the cleanup work for you. Scoping Most procedural languages have the concept of scope. This determines both the visibility and lifetime of the names defined within that scope. In C, C++, and Java, scope is determined by the placement of curly braces {}. So for example:
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
A variable defined within a scope is available only to the end of that scope. Any text after a ‘//’ to the end of a line is a comment. Indentation makes Java code easier to read. Since Java is a free-form language, the extra spaces, tabs, and carriage returns do not affect the resulting program. You cannot do the following, even though it is legal in C and C++:
```java
{
int x = 12;
{
```

<!--p68-->
Everything Is an Object
```java
int x = 96; // Illegal
}
}
```
The compiler will announce that the variable x has already been defined. Thus the C and C++ ability to “hide” a variable in a larger scope is not allowed, because the Java designers thought that it led to confusing programs. Scope of objects Java objects do not have the same lifetimes as primitives. When you create a Java object using new, it hangs around past the end of the scope. Thus if you use:
```java
{
String s = new String("a string");
} // End of scope
```
the reference s vanishes at the end of the scope. However, the String object that s was pointing to is still occupying memory. In this bit of code, there is no way to access the object after the end of the scope, because the only reference to it is out of scope. In later chapters you’ll see how the reference to the object can be passed around and duplicated during the course of a program. It turns out that because objects created with new stay around for as long as you want them, a whole slew of C++ programming problems simply vanish in Java. In C++ you must not only make sure that the objects stay around for as long as you need them, you must also destroy the objects when you’re done with them. That brings up an interesting question. If Java leaves the objects lying around, what keeps them from filling up memory and halting your program? This is exactly the kind of problem that would occur in C++. This is where a bit of magic happens. Java has a garbage collector, which looks at all the objects that were created with new and figures out which ones are not being referenced anymore. Then it releases the memory for those objects, so the memory can be used for new objects. This means that you never need to worry about reclaiming memory yourself. You simply create objects, and when you no longer need them, they will go away by themselves. This eliminates a certain class of programming problem: the so-called “memory leak,” in which a programmer forgets to release memory.
## Creating new data types: class
If everything is an object, what determines how a particular class of object looks and behaves? Put another way, what establishes the type of an object? You might expect there to be a keyword called “type,” and that certainly would have made sense. Historically, however, most objectoriented languages have used the keyword class to mean “I’m about to tell you what a new type of object looks like.” The class keyword (which is so common that it will not usually be boldfaced throughout this book) is followed by the name of the new type. For example:
```java
class ATypeName { /* Class body goes here */ }
```
This introduces a new type, although the class body consists only of a comment (the stars and slashes and what is inside, which will be discussed later in this chapter), so there is not too much that you can do with it. However, you can create an object of this type using new:

<!--p69-->
```java
ATypeName a = new ATypeName();
```
But you cannot tell it to do much of anything (that is, you cannot send it any interesting messages) until you define some methods for it. Fields and methods When you define a class (and all you do in Java is define classes, make objects of those classes, and send messages to those objects), you can put two types of elements in your class: fields (sometimes called data members), and methods (sometimes called member functions). A field is an object of any type that you can talk to via its reference, or a primitive type. If it is a reference to an object, you must initialize that reference to connect it to an actual object (using new, as seen earlier). Each object keeps its own storage for its fields; ordinary fields are not shared among objects. Here is an example of a class with some fields:
```java
class DataOnly {
int i;
double d;
boolean b;
}
```
This class doesn’t do anything except hold data. But you can create an object like this:
```java
DataOnly data = new DataOnly();
```
You can assign values to the fields, but you must first know how to refer to a member of an object. This is accomplished by stating the name of the object reference, followed by a period (dot), followed by the name of the member inside the object:
```java
objectReference.member
```
For example:
```java
data.i = 47;
data.d = 1.1;
data.b = false;
```
It is also possible that your object might contain other objects that contain data you’d like to modify. For this, you just keep “connecting the dots.” For example:
```java
myPlane.leftTank.capacity = 100;
```

<!--p70-->
The DataOnly class cannot do much of anything except hold data, because it has no methods. To understand how those work, you must first understand arguments and return values, which will be described shortly. Default values for primitive members When a primitive data type is a member of a class, it is guaranteed to get a default value if you do not initialize it: Primitive type Default boolean false char ‘\u0000’ (null) Everything Is an Object Primitive type Default byte (byte)0 short (short)0 int long 0L float 0.0f double 0.0d The default values are only what Java guarantees when the variable is used as a member of a class. This ensures that member variables of primitive types will always be initialized (something C++ doesn’t do), reducing a source of bugs. However, this initial value may not be correct or even legal for the program you are writing. It’s best to always explicitly initialize your variables. This guarantee doesn’t apply to local variables—those that are not fields of a class. Thus, if within a method definition you have:
```java
int x;
```
Then x will get some arbitrary value (as in C and C++); it will not automatically be initialized to zero. You are responsible for assigning an appropriate value before you use x. If you forget, Java definitely improves on C++: You get a compile-time error telling you the variable might not have been initialized. (Many C++ compilers will warn you about uninitialized variables, but in Java these are errors.) Methods, arguments, and return values In many languages (like C and C++), the term function is used to describe a named subroutine. The term that is more commonly used in Java is method, as in “a way to do something.” If you want, you can continue thinking in terms of functions. It’s really only a syntactic difference, but this book follows the common Java usage of the term “method.” Methods in Java determine the messages an object can receive. The fundamental parts of a method are the name, the arguments, the return type, and the body. Here is the basic form:
```java
ReturnType methodName( /* Argument list */ ) {
/* Method body */
}
```

<!--p71-->
The return type describes the value that comes back from the method after you call it. The argument list gives the types and names for the information that you want to pass into the method. The method name and argument list (which is called the signature of the method) uniquely identify that method. Methods in Java can be created only as part of a class. A method can be called only for an object,3 and that object must be able to perform that method call. If you try to call the wrong method for an object, you’ll get an error message at compile time. You call a method for an object by naming the object followed by a period (dot), followed by the name of the method and its argument list, like this: 3static methods, which you’ll learn about soon, can be called for the class, without an object.
```java
objectName.methodName(arg1, arg2, arg3);
```
For example, suppose you have a method f( ) that takes no arguments and returns a value of type int. Then, if you have an object called a for which f( ) can be called, you can say this:
```java
int x = a.f();
```
The type of the return value must be compatible with the type of x. This act of calling a method is commonly referred to as sending a message to an object. In the preceding example, the message is f( ) and the object is a. Object-oriented programming is often summarized as simply “sending messages to objects.” The argument list The method argument list specifies what information you pass into the method. As you might guess, this information—like everything else in Java—takes the form of objects. So, what you must specify in the argument list are the types of the objects to pass in and the name to use for each one. As in any situation in Java where you seem to be handing objects around, you are actually passing references.4 The type of the reference must be correct, however. If the argument is supposed to be a String, you must pass in a String or the compiler will give an error. Consider a method that takes a String as its argument. Here is the definition, which must be placed within a class definition for it to be compiled:
```java
int storage(String s) {
return s.length() * 2;
}
```
This method tells you how many bytes are required to hold the information in a particular String. (The size of each char in a String is 16 bits, or two bytes, to support Unicode characters.) The argument is of type String and is called s. Once s is passed into the method, you can treat it just like any other object. (You can send messages to it.) Here, the length( ) method is called, which is one of the methods for Strings; it returns the number of characters in a string. You can also see the use of the return keyword, which does two things. First, it means “Leave the method, I’m done.” Second, if the method produces a value, that value is placed right after the return statement. In this case, the return value is produced by evaluating the expression s.length( ) * 2. You can return any type you want, but if you don’t want to return anything at all, you do so by indicating that the method returns void. Here are some examples:
```java
boolean flag() { return true; }
double naturalLogBase() { return 2.718; }
void nothing() { return; }
void nothing2() {}
```

<!--p72-->

<!--p73-->
When the return type is void, then the return keyword is used only to exit the method, and is therefore unnecessary when you reach the end of the method. You can return from a method at any point, but if you’ve given a non-void return type, then the compiler will force you (with error messages) to return the appropriate type of value regardless of where you return. At this point, it can look like a program is just a bunch of objects with methods that take other objects as arguments and send messages to those other objects. That is indeed much of Everything Is an Object what goes on, but in the following chapter you’ll learn how to do the detailed low-level work by making decisions within a method. For this chapter, sending messages will suffice. Building a Java program There are several other issues you must understand before seeing your first Java program. Name visibility A problem in any programming language is the control of names. If you use a name in one module of the program, and another programmer uses the same name in another module, how do you distinguish one name from another and prevent the two names from “clashing”? In C this is a particular problem because a program is often an unmanageable sea of names. C++ classes (on which Java classes are based) nest functions within classes so they cannot clash with function names nested within other classes. However, C++ still allows global data and global functions, so clashing is still possible. To solve this problem, C++ introduced namespaces using additional keywords. Java was able to avoid all of this by taking a fresh approach. To produce an unambiguous name for a library, the Java creators want you to use your Internet domain name in reverse since domain names are guaranteed to be unique. Since my domain name is MindView.net, my utility library of foibles would be named net.mindview.utility.foibles. After your reversed domain name, the dots are intended to represent subdirectories. In Java 1.0 and Java 1.1 the domain extensions com, edu, org, net, etc., were capitalized by convention, so the library would appear: NET.mindview.utility.foibles. Partway through the development of Java 2, however, it was discovered that this caused problems, so now the entire package name is lowercase. This mechanism means that all of your files automatically live in their own namespaces, and each class within a file must have a unique identifier—the language prevents name clashes for you. Using other components Whenever you want to use a predefined class in your program, the compiler must know how to locate it. Of course, the class might already exist in the same source-code file that it’s being called from. In that case, you simply use the class—even if the class doesn’t get defined until later in the file (Java eliminates the so-called “forward referencing” problem). What about a class that exists in some other file? You might think that the compiler should be smart enough to simply go and find it, but there is a problem. Imagine that you want to use a class with a particular name, but more than one definition for that class exists (presumably these are different definitions). Or worse, imagine that you’re writing a program, and as you’re building it you add a new class to your library that conflicts with the name of an existing class. To solve this problem, you must eliminate all potential ambiguities. This is accomplished by telling the Java compiler exactly what classes you want by using the import keyword. import tells the compiler to bring in a package, which is a library of classes. (In other languages, a library could consist of functions and data as well as classes, but remember that all code in Java must be written inside a class.) Everything Is an Object Most of the time you’ll be using components from the standard Java libraries that come with your compiler. With these, you don’t need to worry about long, reversed domain names; you just say, for example:
```java
import java.util.ArrayList;
```
to tell the compiler that you want to use Java’s ArrayList class. However, util contains a number of classes, and you might want to use several of them without declaring them all explicitly. This is easily accomplished by using ‘*’ to indicate a wild card:
```java
import java.util.*;
```
It is more common to import a collection of classes in this manner than to import classes individually.
## The static keyword
Ordinarily, when you create a class you are describing how objects of that class look and how they will behave. You don’t actually get an object until you create one using new, and at that point storage is allocated and methods become available. There are two situations in which this approach is not sufficient. One is if you want to have only a single piece of storage for a particular field, regardless of how many objects of that class are created, or even if no objects are created. The other is if you need a method that isn’t associated with any particular object of this class. That is, you need a method that you can call even if no objects are created. You can achieve both of these effects with the static keyword. When you say something is static, it means that particular field or method is not tied to any particular object instance of that class. So even if you’ve never created an object of that class you can call a static method or access a static field. With ordinary, non-static fields and methods, you must create an object and use that object to access the field or method, since non-static fields and methods must know the particular object they are working with.4 Some object-oriented languages use the terms class data and class methods, meaning that the data and methods exist only for the class as a whole, and not for any particular objects of the class. Sometimes the Java literature uses these terms too. To make a field or method static, you simply place the keyword before the definition. For example, the following produces a static field and initializes it:
```java
class StaticTest {
static int i = 47;
}
```
Now even if you make two StaticTest objects, there will still be only one piece of storage for StaticTest.i. Both objects will share the same i. Consider:
```java
StaticTest st1 = new StaticTest();
StaticTest st2 = new StaticTest();
```

<!--p74-->
4Of course, since static methods don’t need any objects to be created before they are used, they cannot directly access non-static members or methods by simply calling those other members without referring to a named object (since non- static members and methods must be tied to a particular object). At this point, both st1.i and st2.i have the same value of 47 since they refer to the same piece of memory. There are two ways to refer to a static variable. As the preceding example indicates, you can name it via an object, by saying, for example, st2.i. You can also refer to it directly through its class name, something you cannot do with a non-static member.
```java
StaticTest.i++;
```
The ++ operator adds one to the variable. At this point, both st1.i and st2.i will have the value 48. Using the class name is the preferred way to refer to a static variable. Not only does it emphasize that variable’s static nature, but in some cases it gives the compiler better opportunities for optimization. Similar logic applies to static methods. You can refer to a static method either through an object as you can with any method, or with the special additional syntax ClassName.method( ). You define a static method in a similar way:
```java
class Incrementable {
static void increment() { StaticTest.i++; }
}
```
You can see that the Incrementable method increment( ) increments the static data i using the ++ operator. You can call increment( ) in the typical way, through an object:
```java
Incrementable sf = new Incrementable();
sf.increment();
```
Or, because increment( ) is a static method, you can call it directly through its class:
```java
Incrementable.increment();
```
Although static, when applied to a field, definitely changes the way the data is created (one for each class versus the non-static one for each object), when applied to a method it’s not so dramatic. An important use of static for methods is to allow you to call that method without creating an object. This is essential, as you will see, in defining the main( ) method that is the entry point for running an application. Your first Java program Finally, here’s the first complete program. It starts by printing a string, and then the date, using the Date class from the Java standard library.

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
Everything Is an Object At the beginning of each program file, you must place any necessary import statements to bring in extra classes you’ll need for the code in that file. Note that I say “extra”. That’s because there’s a certain library of classes that are automatically brought into every Java file: java.lang. Start up your Web browser and look at the documentation from Sun. (If you haven’t downloaded the JDK documentation from http://java.sun.com, do so now.5Note that this documentation doesn’t come packed with the JDK; you must do a separate download to get it.) If you look at the list of the packages, you’ll see all the different class libraries that come with Java. Select java.lang. This will bring up a list of all the classes that are part of that library. Since java.lang is implicitly included in every Java code file, these classes are automatically available. There’s no Date class listed in java.lang, which means you must import another library to use that. If you don’t know the library where a particular class is, or if you want to see all of the classes, you can select “Tree” in the Java documentation. Now you can find every single class that comes with Java. Then you can use the browser’s “find” function to find Date. When you do you’ll see it listed as java.util.Date, which lets you know that it’s in the util library and that you must import java.util.* in order to use Date. If you go back to the beginning, select java.lang and then System, you’ll see that the System class has several fields, and if you select out, you’ll discover that it’s a static PrintStream object. Since it’s static, you don’t need to create anything with new. The out object is always there, and you can just use it. What you can do with this out object is determined by its type: PrintStream. Conveniently, PrintStream is shown in the description as a hyperlink, so if you click on that, you’ll see a list of all the methods you can call for PrintStream. There are quite a few, and these will be covered later in the book. For now all we’re interested in is println( ), which in effect means “Print what I’m giving you out to the console and end with a newline.” Thus, in any Java program you write you can write something like this:
```java
System.out.println("A String of things");
```
whenever you want to display information to the console. The name of the class is the same as the name of the file. When you’re creating a standalone program such as this one, one of the classes in the file must have the same name as the file. (The compiler complains if you don’t do this.) That class must contain a method called main( ) with this signature and return type:
```java
public static void main(String[] args) {
```
The public keyword means that the method is available to the outside world (described in detail in the Access Control chapter). The argument to main( ) is an array of String objects. The args won’t be used in this program, but the Java compiler insists that they be there because they hold the arguments from the command line. The line that prints the date is quite interesting:
```java
System.out.println(new Date());
```

<!--p76-->
The argument is a Date object that is being created just to send its value (which is automatically converted to a String) to println( ). As soon as this statement is finished, that Date is unnecessary, and the garbage collector can come along and get it anytime. We don’t need to worry about cleaning it up. 5The Java compiler and documentation from Sun tend to change regularly, and the best place to get them is directly from Sun. By downloading it yourself, you will get the most recent version. When you look at the JDK documentation from http://java.sun.com, you will see that System has many other methods that allow you to produce interesting effects (one of Java’s most powerful assets is its large set of standard libraries). For example:
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
The first line in main( ) displays all of the “properties” from the system where you are running the program, so it gives you environment information. The list( ) method sends the results to its argument, System.out. You will see later in the book that you can send the results elsewhere, to a file, for example. You can also ask for a specific property—in this case, the user name and java.library.path. (The unusual comments at the beginning and end will be explained a little later.) Compiling and running To compile and run this program, and all the other programs in this book, you must first have a Java programming environment. There are a number of third-party development environments, but in this book I will assume that you are using the Java Developer’s Kit (JDK) from Sun, which is free. If you are using another development system,6you will need to look in the documentation for that system to determine how to compile and run programs. Get on the Internet and go to http://java.sun.com. There you will find information and links that will lead you through the process of downloading and installing the JDK for your particular platform. Once the JDK is installed, and you’ve set up your computer’s path information so that it will find javac and java, download and unpack the source code for this book (you can find it at www.MindView.net). This will create a subdirectory for each chapter in this book. Move to the subdirectory named objects and type:
```java
javac HelloDate.java
```
This command should produce no response. If you get any kind of an error message, it means you haven’t installed the JDK properly and you need to investigate those problems. On the other hand, if you just get your command prompt back, you can type:
```java
java HelloDate
```

<!--p77-->
and you’ll get the message and the date as output. This is the process you can use to compile and run each of the programs in this book. However, you will see that the source code for this book also has a file called build.xml in each chapter, and this contains “Ant” commands for automatically building the files for that 6IBM’s “jikes” compiler is a common alternative, as it is significantly faster than Sun’s javac (although if you’re building groups of files using Ant, there’s not too much of a difference). There are also open-source projects to create Java compilers, runtime environments, and libraries. chapter. Buildfiles and Ant (including where to download it) are described more fully in the supplement you will find at http://MindView.net/Books/BetterJava, but once you have Ant installed (from http://jakarta.apache.org/ant) you can just type ‘ant’ at the command prompt to compile and run the programs in each chapter. If you haven’t installed Ant yet, you can just type the javac and java commands by hand. Comments and embedded documentation There are two types of comments in Java. The first is the traditional C-style comment that was inherited by C++. These comments begin with a /* and continue, possibly across many lines, until a */. Note that many programmers will begin each line of a continued comment with a *, so you’ll often see:
```java
/* This is a comment
* that continues
* across lines
*/
```
Remember, however, that everything inside the /* and */ is ignored, so there’s no difference in saying:
```java
/* This is a comment that
continues across lines */
```
The second form of comment comes from C++. It is the single-line comment, which starts with a // and continues until the end of the line. This type of comment is convenient and commonly used because it’s easy. You don’t need to hunt on the keyboard to find / and then * (instead, you just press the same key twice), and you don’t need to close the comment. So you will often see:
```java
// This is a one-line comment
```

<!--p78-->
Comment documentation Possibly the biggest problem with documenting code has been maintaining that documentation. If the documentation and the code are separate, it becomes tedious to change the documentation every time you change the code. The solution seems simple: Link the code to the documentation. The easiest way to do this is to put everything in the same file. To complete the picture, however, you need a special comment syntax to mark the documentation and a tool to extract those comments and put them in a useful form. This is what Java has done. The tool to extract the comments is called Javadoc, and it is part of the JDK installation. It uses some of the technology from the Java compiler to look for special comment tags that you put in your programs. It not only extracts the information marked by these tags, but it also pulls out the class name or method name that adjoins the comment. This way you can get away with the minimal amount of work to generate decent program documentation. The output of Javadoc is an HTML file that you can view with your Web browser. Thus, Javadoc allows you to create and maintain a single source file and automatically generate useful documentation. Because of Javadoc, you have a straightforward standard for creating documentation, so you can expect or even demand documentation with all Java libraries. Everything Is an Object In addition, you can write your own Javadoc handlers, called doclets, if you want to perform special operations on the information processed by Javadoc (to produce output in a different format, for example). Doclets are introduced in the supplement at http://MindView.net/Books/BetterJava. What follows is only an introduction and overview of the basics of Javadoc. A thorough description can be found in the JDK documentation. When you unpack the documentation, look in the “tooldocs” subdirectory (or follow the “tooldocs” link). Syntax All of the Javadoc commands occur only within /** comments. The comments end with */ as usual. There are two primary ways to use Javadoc: Embed HTML or use “doc tags.” Standalone doc tags are commands that start with an ‘@’ and are placed at the beginning of a comment line. (A leading ‘*’, however, is ignored.) Inline doc tags can appear anywhere within a Javadoc comment and also start with an ‘@’ but are surrounded by curly braces. There are three “types” of comment documentation, which correspond to the element the comment precedes: class, field, or method. That is, a class comment appears right before the definition of a class, a field comment appears right in front of the definition of a field, and a method comment appears right in front of the definition of a method. As a simple example:
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
Note that Javadoc will process comment documentation for only public and protected members. Comments for private and package-access members (see the Access Control chapter) are ignored, and you’ll see no output. (However, you can use the -private flag to include private members as well.) This makes sense, since only public and protected members are available outside the file, which is the client programmer’s perspective. The output for the preceding code is an HTML file that has the same standard format as all the rest of the Java documentation, so users will be comfortable with the format and can easily navigate your classes. It’s worth entering the preceding code, sending it through Javadoc, and viewing the resulting HTML file to see the results. Embedded HTML Javadoc passes HTML commands through to the generated HTML document. This allows you full use of HTML; however, the primary motive is to let you format code, such as:
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
You can also use HTML just as you would in any other Web document to format the regular text in your descriptions:
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
Note that within the documentation comment, asterisks at the beginning of a line are thrown away by Javadoc, along with leading spaces. Javadoc reformats everything so that it conforms to the standard documentation appearance. Don’t use headings such as <h1> or <hr> as embedded HTML, because Javadoc inserts its own headings and yours will interfere with them. All types of comment documentation—class, field, and method—can support embedded HTML. Some example tags Here are some of the Javadoc tags available for code documentation. Before trying to do anything serious using Javadoc, you should consult the Javadoc reference in the JDK documentation to learn all the different ways that you can use Javadoc. @see This tag allows you to refer to the documentation in other classes. Javadoc will generate HTML with the @see tags hyperlinked to the other documentation. The forms are:
```java
@see classname
@see fully-qualified-classname
@see fully-qualified-classname#method-name
```

<!--p80-->
Each one adds a hyperlinked “See Also” entry to the generated documentation. Javadoc will not check the hyperlinks you give it to make sure they are valid. {@link package.class#member label} Very similar to @see, except that it can be used inline and uses the label as the hyperlink text rather than “See Also.” {@docRoot} Produces the relative path to the documentation root directory. Useful for explicit hyperlinking to pages in the documentation tree. {@inheritDoc} Inherits the documentation from the nearest base class of this class into the current doc comment. Everything Is an Object @version This is of the form:
```java
@version version-information
```
in which version-information is any significant information you see fit to include. When the - version flag is placed on the Javadoc command line, the version information will be called out specially in the generated HTML documentation. @author This is of the form:
```java
@author author-information
```
in which author-information is, presumably, your name, but it could also include your email address or any other appropriate information. When the -author flag is placed on the Javadoc command line, the author information will be called out specially in the generated HTML documentation. You can have multiple author tags for a list of authors, but they must be placed consecutively. All the author information will be lumped together into a single paragraph in the generated HTML. @since This tag allows you to indicate the version of this code that began using a particular feature. You’ll see it appearing in the HTML Java documentation to indicate what version of the JDK is used. @param This is used for method documentation, and is of the form:
```java
@param parameter-name description
```
in which parameter-name is the identifier in the method parameter list, and description is text that can continue on subsequent lines. The description is considered finished when a new documentation tag is encountered. You can have any number of these, presumably one for each parameter. @return This is used for method documentation, and looks like this:
```java
@return description
```

<!--p81-->
in which description gives you the meaning of the return value. It can continue on subsequent lines. @throws Exceptions will be demonstrated in the Error Handling with Exceptions chapter. Briefly, they are objects that can be “thrown” out of a method if that method fails. Although only one exception object can emerge when you call a method, a particular method might produce any number of different types of exceptions, all of which need descriptions. So the form for the exception tag is:
```java
@throws fully-qualified-class-name description
```
in which fully-qualified-class-name gives an unambiguous name of an exception class that’s defined somewhere, and description (which can continue on subsequent lines) tells you why this particular type of exception can emerge from the method call. @deprecated This is used to indicate features that were superseded by an improved feature. The deprecated tag is a suggestion that you no longer use this particular feature, since sometime in the future it is likely to be removed. A method that is marked @deprecated causes the compiler to issue a warning if it is used. In Java SE5, the @deprecated Javadoc tag has been superseded by the @Deprecated annotation (you’ll learn about these in the Annotations chapter). Documentation example Here is the first Java program again, this time with documentation comments added:
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
The first line of the file uses my own technique of putting a ‘//:’ as a special marker for the comment line containing the source file name. That line contains the path information to the file (object indicates this chapter) followed by the file name. The last line also finishes with a comment, and this one (‘///:~’) indicates the end of the source code listing, which allows it to be automatically updated into the text of this book after being checked with a compiler and executed. Everything Is an Object The /* Output: tag indicates the beginning of the output that will be generated by this file. In this form, it can be automatically tested to verify its accuracy. In this case, the (55% match)indicates to the testing system that the output will be fairly different from one run to the next so it should only expect a 55 percent correlation with the output shown here. Most examples in this book that produce output will contain the output in this commented form, so you can see the output and know that it is correct. Coding style The style described in the Code Conventions for the Java Programming Language7is to capitalize the first letter of a class name. If the class name consists of several words, they are run together (that is, you don’t use underscores to separate the names), and the first letter of each embedded word is capitalized, such as:
```java
class AllTheColorsOfTheRainbow { // ...
```
This is sometimes called “camel-casing.” For almost everything else—methods, fields (member variables), and object reference names—the accepted style is just as it is for classes except that the first letter of the identifier is lowercase. For example:
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
The user must also type all these long names, so be merciful. The Java code you will see in the Sun libraries also follows the placement of open-and-close curly braces that you see used in this book. Summary The goal of this chapter is just enough Java to understand how to write a simple program. You’ve also gotten an overview of the language and some of its basic ideas. However, the examples so far have all been of the form “Do this, then do that, then do something else.” The next two chapters will introduce the basic operators used in Java programming, and then show you how to control the flow of your program. Exercises Normally, exercises will be distributed throughout the chapters, but in this chapter you were learning how to write basic programs so all the exercises were delayed until the end. The number in parentheses after each exercise number is an indicator of how difficult the exercise is, in a ranking from 1-10. Solutions to selected exercises can be found in the electronic document The Thinking in Java Annotated Solution Guide, available for sale from www.MindView.net. 7http://java.sun.com/docs/codeconv/index.html. To preserve space in this book and seminar presentations, not all of these guidelines could be followed, but you’ll see that the style I use here matches the Java standard as much as possible. Exercise 1: (2) Create a class containing an int and a char that are not initialized, and print their values to verify that Java performs default initialization. Exercise 2: (1) Following the HelloDate.java example in this chapter, create a “hello, world” program that simply displays that statement. You need only a single method in your class (the “main” one that gets executed when the program starts). Remember to make it static and to include the argument list, even though you don’t use the argument list. Compile the program with javac and run it using java. If you are using a different development environment than the JDK, learn how to compile and run programs in that environment. Exercise 3: (1) Find the code fragments involving ATypeName and turn them into a program that compiles and runs. Exercise 4: (1) Turn the DataOnly code fragments into a program that compiles and runs. Exercise 5: (1) Modify the previous exercise so that the values of the data in DataOnly are assigned to and printed in main( ). Exercise 6: (2) Write a program that includes and calls the storage( ) method defined as a code fragment in this chapter. Exercise 7: (1) Turn the Incrementable code fragments into a working program. Exercise 8: (3) Write a program that demonstrates that, no matter how many objects you create of a particular class, there is only one instance of a particular static field in that class. Exercise 9: (2) Write a program that demonstrates that autoboxing works for all the primitive types and their wrappers. Exercise 10: (2) Write a program that prints three arguments taken from the command line. To do this, you’ll need to index into the command-line array of Strings. Exercise 11: (1) Turn the AllTheColorsOfTheRainbow example into a program that compiles and runs. Exercise 12: (2) Find the code for the second version of HelloDate.java, which is the simple comment documentation example. Execute Javadoc on the file and view the results with your Web browser. Exercise 13: (1) Run Documentation1.java, Documentation2.java, and Documentation3.java through Javadoc. Verify the resulting documentation with your Web browser. Exercise 14: (1) Add an HTML list of items to the documentation in the previous exercise. Exercise 15: (1) Take the program in Exercise 2 and add comment documentation to it. Extract this comment documentation into an HTML file using Javadoc and view it with your Web browser. Everything Is an Object Exercise 16: (1) In the Initialization & Cleanup chapter, locate the Overloading.java example and add Javadoc documentation. Extract this comment documentation into an HTML file using Javadoc and view it with your Web browser.