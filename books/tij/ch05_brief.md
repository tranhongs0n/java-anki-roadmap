# 5. Initialization & Cleanup (printed p107-144)


<!--p129-->
Initialization & Cleanup As the computer revolution progresses, “unsafe” programming has become one of the major culprits that makes programming expensive. Two of these safety issues are initialization and cleanup. Many C bugs occur when the programmer forgets to initialize a variable. This is especially true with libraries when users don’t know how to initialize a library component, or even that they must. Cleanup is a special problem because it’s easy to forget about an element when you’re done with it, since it no longer concerns you. Thus, the resources used by that element are retained and you can easily end up running out of resources (most notably, memory). C++ introduced the concept of a constructor, a special method automatically called when an object is created. Java also adopted the constructor, and in addition has a garbage collector that automatically releases memory resources when they’re no longer being used. This chapter examines the issues of initialization and cleanup, and their support in Java. Guaranteed initialization with the constructor You can imagine creating a method called initialize( ) for every class you write. The name is a hint that it should be called before using the object. Unfortunately, this means the user must remember to call that method. In Java, the class designer can guarantee initialization of every object by providing a constructor. If a class has a constructor, Java automatically calls that constructor when an object is created, before users can even get their hands on it. So initialization is guaranteed. The next challenge is what to name this method. There are two issues. The first is that any name you use could clash with a name you might like to use as a member in the class. The second is that because the compiler is responsible for calling the constructor, it must always know which method to call. The C++ solution seems the easiest and most logical, so it’s also used in Java: The name of the constructor is the same as the name of the class. It makes sense that such a method will be called automatically during initialization. Here’s a simple class with a constructor:

<!--p130-->
```java
//: initialization/SimpleConstructor.java
// Demonstration of a simple constructor.
class Rock {
Rock() { // This is the constructor
System.out.print("Rock ");
}
}
public class SimpleConstructor {
public static void main(String[] args) {
for(int i = 0; i < 10; i++)
new Rock();
}
} /* Output:
Rock Rock Rock Rock Rock Rock Rock Rock Rock Rock
*///:~
```
Now, when an object is created:
```java
new Rock();
```
storage is allocated and the constructor is called. It is guaranteed that the object will be properly initialized before you can get your hands on it. Note that the coding style of making the first letter of all methods lowercase does not apply to constructors, since the name of the constructor must match the name of the class exactly. A constructor that takes no arguments is called the default constructor. The Java documents typically use the term no-arg constructor, but “default constructor” has been in use for many years before Java appeared, so I will tend to use that. But like any method, the constructor can also have arguments to allow you to specify how an object is created. The preceding example can easily be changed so the constructor takes an argument:
```java
//: initialization/SimpleConstructor2.java
// Constructors can have arguments.
class Rock2 {
Rock2(int i) {
System.out.print("Rock " + i + " ");
}
}
public class SimpleConstructor2 {
public static void main(String[] args) {
for(int i = 0; i < 8; i++)
new Rock2(i);
}
} /* Output:
Rock 0 Rock 1 Rock 2 Rock 3 Rock 4 Rock 5 Rock 6 Rock 7
*///:~
```
Constructor arguments provide you with a way to provide parameters for the initialization of an object. For example, if the class Tree has a constructor that takes a single integer argument denoting the height of the tree, you create a Tree object like this:
```java
Tree t = new Tree(12); // 12-foot tree
```

<!--p131-->
If Tree(int) is your only constructor, then the compiler won’t let you create a Tree object any other way. Constructors eliminate a large class of problems and make the code easier to read. In the preceding code fragment, for example, you don’t see an explicit call to some initialize( ) method that is conceptually separate from creation. In Java, creation and initialization are unified concepts—you can’t have one without the other. The constructor is an unusual type of method because it has no return value. This is distinctly different from a void return value, in which the method returns nothing but you still have the option to make it return something else. Constructors return nothing and you don’t have an option (the new expression does return a reference to the newly created object, but the constructor itself has no return value). If there were a return value, and if you could select your own, the compiler would somehow need to know what to do with that return value. Exercise 1: (1) Create a class containing an uninitialized String reference. Demonstrate that this reference is initialized by Java to null. Exercise 2: (2) Create a class with a String field that is initialized at the point of definition, and another one that is initialized by the constructor. What is the difference between the two approaches? Method overloading One of the important features in any programming language is the use of names. When you create an object, you give a name to a region of storage. A method is a name for an action. You refer to all objects and methods by using names. Well-chosen names create a system that is easier for people to understand and change. It’s a lot like writing prose—the goal is to communicate with your readers. A problem arises when mapping the concept of nuance in human language onto a programming language. Often, the same word expresses a number of different meanings—it’s overloaded. This is useful, especially when it comes to trivial differences. You say, “Wash the shirt,” “Wash the car,” and “Wash the dog.” It would be silly to be forced to say, “shirtWash the shirt,” “carWash the car,” and “dogWash the dog” just so the listener doesn’t need to make any distinction about the action performed. Most human languages are redundant, so even if you miss a few words, you can still determine the meaning. You don’t need unique identifiers—you can deduce meaning from context. Most programming languages (C in particular) require you to have a unique identifier for each method (often called functions in those languages). So you could not have one function called print( ) for printing integers and another called print( ) for printing floats—each function requires a unique name. In Java (and C++), another factor forces the overloading of method names: the constructor. Because the constructor’s name is predetermined by the name of the class, there can be only one constructor name. But what if you want to create an object in more than one way? For example, suppose you build a class that can initialize itself in a standard way or by reading information from a file. You need two constructors, the default constructor and one that takes a String as an argument, which is the name of the file from which to initialize the object. Both are constructors, so they must have the same name—the name of the class. Thus, method overloading is essential to allow the same method name to be used with different argument types. And although method overloading is a must for constructors, it’s a general convenience and can be used with any method. Here’s an example that shows both overloaded constructors and overloaded methods:
```java
//: initialization/Overloading.java
// Demonstration of both constructor
// and ordinary method overloading.
import static net.mindview.util.Print.*;
class Tree {
int height;
Tree() {
print("Planting a seedling");
height = 0;
}
Tree(int initialHeight) {
height = initialHeight;
print("Creating new Tree that is " +
height + " feet tall");
```

<!--p132-->
Initialization & Cleanup
```java
}
void info() {
print("Tree is " + height + " feet tall");
}
void info(String s) {
print(s + ": Tree is " + height + " feet tall");
}
}
public class Overloading {
public static void main(String[] args) {
for(int i = 0; i < 5; i++) {
Tree t = new Tree(i);
t.info();
t.info("overloaded method");
}
// Overloaded constructor:
new Tree();
}
} /* Output:
Creating new Tree that is 0 feet tall
Tree is 0 feet tall
overloaded method: Tree is 0 feet tall
Creating new Tree that is 1 feet tall
Tree is 1 feet tall
overloaded method: Tree is 1 feet tall
Creating new Tree that is 2 feet tall
Tree is 2 feet tall
overloaded method: Tree is 2 feet tall
Creating new Tree that is 3 feet tall
Tree is 3 feet tall
overloaded method: Tree is 3 feet tall
Creating new Tree that is 4 feet tall
Tree is 4 feet tall
overloaded method: Tree is 4 feet tall
Planting a seedling
*///:~
```

<!--p133-->
A Tree object can be created either as a seedling, with no argument, or as a plant grown in a nursery, with an existing height. To support this, there is a default constructor, and one that takes the existing height. You might also want to call the info( ) method in more than one way. For example, if you have an extra message you want printed, you can use info(String), and info( ) if you have nothing more to say. It would seem strange to give two separate names to what is obviously the same concept. Fortunately, method overloading allows you to use the same name for both. Distinguishing overloaded methods If the methods have the same name, how can Java know which method you mean? There’s a simple rule: Each overloaded method must take a unique list of argument types. If you think about this for a second, it makes sense. How else could a programmer tell the difference between two methods that have the same name, other than by the types of their arguments? Even differences in the ordering of arguments are sufficient to distinguish two methods, although you don’t normally want to take this approach because it produces difficult-to- maintain code:
```java
//: initialization/OverloadingOrder.java
// Overloading based on the order of the arguments.
import static net.mindview.util.Print.*;
public class OverloadingOrder {
static void f(String s, int i) {
print("String: " + s + ", int: " + i);
}
static void f(int i, String s) {
print("int: " + i + ", String: " + s);
}
public static void main(String[] args) {
f("String first", 11);
f(99, "Int first");
}
} /* Output:
String: String first, int: 11
int: 99, String: Int first
*///:~
```
The two f( ) methods have identical arguments, but the order is different, and that’s what makes them distinct. Overloading with primitives A primitive can be automatically promoted from a smaller type to a larger one, and this can be slightly confusing in combination with overloading. The following example demonstrates what happens when a primitive is handed to an overloaded method:
```java
//: initialization/PrimitiveOverloading.java
// Promotion of primitives and overloading.
import static net.mindview.util.Print.*;
public class PrimitiveOverloading {
void f1(char x) { printnb("f1(char) "); }
void f1(byte x) { printnb("f1(byte) "); }
void f1(short x) { printnb("f1(short) "); }
void f1(int x) { printnb("f1(int) "); }
void f1(long x) { printnb("f1(long) "); }
void f1(float x) { printnb("f1(float) "); }
void f1(double x) { printnb("f1(double) "); }
void f2(byte x) { printnb("f2(byte) "); }
void f2(short x) { printnb("f2(short) "); }
void f2(int x) { printnb("f2(int) "); }
void f2(long x) { printnb("f2(long) "); }
void f2(float x) { printnb("f2(float) "); }
void f2(double x) { printnb("f2(double) "); }
void f3(short x) { printnb("f3(short) "); }
void f3(int x) { printnb("f3(int) "); }
void f3(long x) { printnb("f3(long) "); }
void f3(float x) { printnb("f3(float) "); }
void f3(double x) { printnb("f3(double) "); }
void f4(int x) { printnb("f4(int) "); }
void f4(long x) { printnb("f4(long) "); }
void f4(float x) { printnb("f4(float) "); }
void f4(double x) { printnb("f4(double) "); }
void f5(long x) { printnb("f5(long) "); }
```

<!--p134-->
Initialization & Cleanup

<!--p135-->
```java
void f5(float x) { printnb("f5(float) "); }
void f5(double x) { printnb("f5(double) "); }
void f6(float x) { printnb("f6(float) "); }
void f6(double x) { printnb("f6(double) "); }
void f7(double x) { printnb("f7(double) "); }
void testConstVal() {
printnb("5: ");
f1(5);f2(5);f3(5);f4(5);f5(5);f6(5);f7(5); print();
}
void testChar() {
char x = ‘x’;
printnb("char: ");
f1(x);f2(x);f3(x);f4(x);f5(x);f6(x);f7(x); print();
}
void testByte() {
byte x = 0;
printnb("byte: ");
f1(x);f2(x);f3(x);f4(x);f5(x);f6(x);f7(x); print();
}
void testShort() {
short x = 0;
printnb("short: ");
f1(x);f2(x);f3(x);f4(x);f5(x);f6(x);f7(x); print();
}
void testInt() {
int x = 0;
printnb("int: ");
f1(x);f2(x);f3(x);f4(x);f5(x);f6(x);f7(x); print();
}
void testLong() {
long x = 0;
printnb("long: ");
f1(x);f2(x);f3(x);f4(x);f5(x);f6(x);f7(x); print();
}
void testFloat() {
float x = 0;
printnb("float: ");
f1(x);f2(x);f3(x);f4(x);f5(x);f6(x);f7(x); print();
}
void testDouble() {
double x = 0;
printnb("double: ");
f1(x);f2(x);f3(x);f4(x);f5(x);f6(x);f7(x); print();
}
public static void main(String[] args) {
PrimitiveOverloading p =
new PrimitiveOverloading();
p.testConstVal();
p.testChar();
p.testByte();
p.testShort();
p.testInt();
p.testLong();
p.testFloat();
p.testDouble();
}
} /* Output:
5: f1(int) f2(int) f3(int) f4(int) f5(long) f6(float) f7(double)
char: f1(char) f2(int) f3(int) f4(int) f5(long) f6(float) f7(double)
byte: f1(byte) f2(byte) f3(short) f4(int) f5(long) f6(float) f7(double)
short: f1(short) f2(short) f3(short) f4(int) f5(long) f6(float)
f7(double)
int: f1(int) f2(int) f3(int) f4(int) f5(long) f6(float) f7(double)
long: f1(long) f2(long) f3(long) f4(long) f5(long) f6(float) f7(double)
float: f1(float) f2(float) f3(float) f4(float) f5(float) f6(float)
f7(double)
double: f1(double) f2(double) f3(double) f4(double) f5(double)
f6(double) f7(double)
*///:~
```
You can see that the constant value 5 is treated as an int, so if an overloaded method is available that takes an int, it is used. In all other cases, if you have a data type that is smaller than the argument in the method, that data type is promoted. char produces a slightly different effect, since if it doesn’t find an exact char match, it is promoted to int. What happens if your argument is bigger than the argument expected by the overloaded method? A modification of the preceding program gives the answer:
```java
//: initialization/Demotion.java
// Demotion of primitives and overloading.
import static net.mindview.util.Print.*;
public class Demotion {
void f1(char x) { print("f1(char)"); }
void f1(byte x) { print("f1(byte)"); }
void f1(short x) { print("f1(short)"); }
void f1(int x) { print("f1(int)"); }
void f1(long x) { print("f1(long)"); }
void f1(float x) { print("f1(float)"); }
void f1(double x) { print("f1(double)"); }
void f2(char x) { print("f2(char)"); }
void f2(byte x) { print("f2(byte)"); }
void f2(short x) { print("f2(short)"); }
void f2(int x) { print("f2(int)"); }
void f2(long x) { print("f2(long)"); }
void f2(float x) { print("f2(float)"); }
void f3(char x) { print("f3(char)"); }
void f3(byte x) { print("f3(byte)"); }
void f3(short x) { print("f3(short)"); }
void f3(int x) { print("f3(int)"); }
void f3(long x) { print("f3(long)"); }
void f4(char x) { print("f4(char)"); }
void f4(byte x) { print("f4(byte)"); }
void f4(short x) { print("f4(short)"); }
void f4(int x) { print("f4(int)"); }
void f5(char x) { print("f5(char)"); }
void f5(byte x) { print("f5(byte)"); }
void f5(short x) { print("f5(short)"); }
void f6(char x) { print("f6(char)"); }
void f6(byte x) { print("f6(byte)"); }
void f7(char x) { print("f7(char)"); }
void testDouble() {
double x = 0;
print("double argument:");
f1(x);f2((float)x);f3((long)x);f4((int)x);
```

<!--p136-->
Initialization & Cleanup
```java
f5((short)x);f6((byte)x);f7((char)x);
}
public static void main(String[] args) {
Demotion p = new Demotion();
p.testDouble();
}
} /* Output:
double argument:
f1(double)
f2(float)
f3(long)
f4(int)
f5(short)
f6(byte)
f7(char)
*///:~
```
Here, the methods take narrower primitive values. If your argument is wider, then you must perform a narrowing conversion with a cast. If you don’t do this, the compiler will issue an error message. Overloading on return values It is common to wonder, “Why only class names and method argument lists? Why not distinguish between methods based on their return values?” For example, these two methods, which have the same name and arguments, are easily distinguished from each other:
```java
void f() {}
int f() { return 1; }
```
This might work fine as long as the compiler could unequivocally determine the meaning from the context, as in int x = f( ). However, you can also call a method and ignore the return value. This is often referred to as calling a method for its side effect, since you don’t care about the return value, but instead want the other effects of the method call. So if you call the method this way:
```java
f();
```
how can Java determine which f( ) should be called? And how could someone reading the code see it? Because of this sort of problem, you cannot use return value types to distinguish overloaded methods. Default constructors As mentioned previously, a default constructor (a.k.a. a “no-arg” constructor) is one without arguments that is used to create a “default object.” If you create a class that has no constructors, the compiler will automatically create a default constructor for you. For example:

<!--p137-->
```java
//: initialization/DefaultConstructor.java
class Bird {}
public class DefaultConstructor {
public static void main(String[] args) {
Bird b = new Bird(); // Default!
}
} ///:~
```
The expression
```java
new Bird()
```
creates a new object and calls the default constructor, even though one was not explicitly defined. Without it, you would have no method to call to build the object. However, if you define any constructors (with or without arguments), the compiler will not synthesize one for you:
```java
//: initialization/NoSynthesis.java
class Bird2 {
Bird2(int i) {}
Bird2(double d) {}
}
public class NoSynthesis {
public static void main(String[] args) {
//! Bird2 b = new Bird2(); // No default
Bird2 b2 = new Bird2(1);
Bird2 b3 = new Bird2(1.0);
}
} ///:~
```
If you say:
```java
new Bird2()
```

<!--p138-->
the compiler will complain that it cannot find a constructor that matches. When you don’t put in any constructors, it’s as if the compiler says, “You are bound to need some constructor, so let me make one for you.” But if you write a constructor, the compiler says, “You’ve written a constructor so you know what you’re doing; if you didn’t put in a default it’s because you meant to leave it out.” Exercise 3:(1) Create a class with a default constructor (one that takes no arguments) that prints a message. Create an object of this class. Exercise 4:(1) Add an overloaded constructor to the previous exercise that takes a String argument and prints it along with your message. Exercise 5: (2) Create a class called Dog with an overloaded bark( ) method. This method should be overloaded based on various primitive data types, and print different types of barking, howling, etc., depending on which overloaded version is called. Write a main( ) that calls all the different versions. Exercise 6:(1) Modify the previous exercise so that two of the overloaded methods have two arguments (of two different types), but in reversed order relative to each other. Verify that this works. Exercise 7:(1) Create a class without a constructor, and then create an object of that class in main( ) to verify that the default constructor is automatically synthesized. Initialization & Cleanup
## The this keyword
If you have two objects of the same type called a and b, you might wonder how it is that you can call a method peel( ) for both those objects:
```java
//: initialization/BananaPeel.java
class Banana { void peel(int i) { /* ... */ } }
public class BananaPeel {
public static void main(String[] args) {
Banana a = new Banana(),
b = new Banana();
a.peel(1);
b.peel(2);
}
} ///:~
```
If there’s only one method called peel( ), how can that method know whether it’s being called for the object a or b? To allow you to write the code in a convenient object-oriented syntax in which you “send a message to an object,” the compiler does some undercover work for you. There’s a secret first argument passed to the method peel( ), and that argument is the reference to the object that’s being manipulated. So the two method calls become something like:
```java
Banana.peel(a, 1);
Banana.peel(b, 2);
```
This is internal and you can’t write these expressions and get the compiler to accept them, but it gives you an idea of what’s happening. Suppose you’re inside a method and you’d like to get the reference to the current object. Since that reference is passed secretly by the compiler, there’s no identifier for it. However, for this purpose there’s a keyword: this. The this keyword—which can be used only inside a non-static method—produces the reference to the object that the method has been called for. You can treat the reference just like any other object reference. Keep in mind that if you’re calling a method of your class from within another method of your class, you don’t need to use this. You simply call the method. The current this reference is automatically used for the other method. Thus you can say:
```java
//: initialization/Apricot.java
public class Apricot {
void pick() { /* ... */ }
void pit() { pick(); /* ... */ }
} ///:~
```

<!--p139-->
Inside pit( ), you could say this.pick( ) but there’s no need to.1 The compiler does it for you automatically. The this keyword is used only for those special cases in which you need to explicitly use the reference to the current object. For example, it’s often used in return statements when you want to return the reference to the current object: 1Some people will obsessively put this in front of every method call and field reference, arguing that it makes it “clearer and more explicit.” Don’t do it. There’s a reason that we use high-level languages: They do things for us. If you put this in when it’s not necessary, you will confuse and annoy everyone who reads your code, since all the rest of the code they’ve read won’t use this everywhere. People expect this to be used only when it is necessary. Following a consistent and straightforward coding style saves time and money.
```java
//: initialization/Leaf.java
// Simple use of the "this" keyword.
public class Leaf {
int i = 0;
Leaf increment() {
i++;
return this;
}
void print() {
System.out.println("i = " + i);
}
public static void main(String[] args) {
Leaf x = new Leaf();
x.increment().increment().increment().print();
}
} /* Output:
i = 3
*///:~
```
Because increment( ) returns the reference to the current object via the this keyword, multiple operations can easily be performed on the same object. The this keyword is also useful for passing the current object to another method:
```java
//: initialization/PassingThis.java
class Person {
public void eat(Apple apple) {
Apple peeled = apple.getPeeled();
System.out.println("Yummy");
}
}
class Peeler {
static Apple peel(Apple apple) {
// ... remove peel
return apple; // Peeled
}
}
class Apple {
Apple getPeeled() { return Peeler.peel(this); }
}
public class PassingThis {
public static void main(String[] args) {
new Person().eat(new Apple());
}
} /* Output:
Yummy
*///:~
```

<!--p140-->
Apple needs to call Peeler.peel( ), which is a foreign utility method that performs an operation that, for some reason, needs to be external to Apple (perhaps the external method can be applied across many different classes, and you don’t want to repeat the code). To pass itself to the foreign method, it must use this. Exercise 8:(1) Create a class with two methods. Within the first method, call the second method twice: the first time without using this, and the second time using this—just to see it working; you should not use this form in practice. Initialization & Cleanup Calling constructors from constructors When you write several constructors for a class, there are times when you’d like to call one constructor from another to avoid duplicating code. You can make such a call by using the this keyword. Normally, when you say this, it is in the sense of “this object” or “the current object,” and by itself it produces the reference to the current object. In a constructor, the this keyword takes on a different meaning when you give it an argument list. It makes an explicit call to the constructor that matches that argument list. Thus you have a straightforward way to call other constructors:
```java
//: initialization/Flower.java
// Calling constructors with "this"
import static net.mindview.util.Print.*;
public class Flower {
int petalCount = 0;
String s = "initial value";
Flower(int petals) {
petalCount = petals;
print("Constructor w/ int arg only, petalCount= "
+ petalCount);
}
Flower(String ss) {
print("Constructor w/ String arg only, s = " + ss);
s = ss;
}
Flower(String s, int petals) {
this(petals);
//! this(s); // Can’t call two!
this.s = s; // Another use of "this"
print("String & int args");
}
Flower() {
this("hi", 47);
print("default constructor (no args)");
}
void printPetalCount() {
//! this(11); // Not inside non-constructor!
print("petalCount = " + petalCount + " s = "+ s);
}
public static void main(String[] args) {
Flower x = new Flower();
x.printPetalCount();
}
} /* Output:
Constructor w/ int arg only, petalCount= 47
String & int args
default constructor (no args)
petalCount = 47 s = hi
*///:~
```

<!--p141-->
The constructor Flower(String s, int petals) shows that, while you can call one constructor using this, you cannot call two. In addition, the constructor call must be the first thing you do, or you’ll get a compiler error message. This example also shows another way you’ll see this used. Since the name of the argument s and the name of the member data s are the same, there’s an ambiguity. You can resolve it Initialization & Cleanup using this.s, to say that you’re referring to the member data. You’ll often see this form used in Java code, and it’s used in numerous places in this book. In printPetalCount( ) you can see that the compiler won’t let you call a constructor from inside any method other than a constructor. Exercise 9:(1) Create a class with two (overloaded) constructors. Using this, call the second constructor inside the first one.
## The meaning of static

<!--p142-->
With the this keyword in mind, you can more fully understand what it means to make a method static. It means that there is no this for that particular method. You cannot call non-static methods from inside static methods2 (although the reverse is possible), and you can call a static method for the class itself, without any object. In fact, that’s primarily what a static method is for. It’s as if you’re creating the equivalent of a global method. However, global methods are not permitted in Java, and putting the static method inside a class allows it access to other static methods and to static fields. Some people argue that static methods are not object-oriented, since they do have the semantics of a global method; with a static method, you don’t send a message to an object, since there’s no this. This is probably a fair argument, and if you find yourself using a lot of static methods, you should probably rethink your strategy. However, statics are pragmatic, and there are times when you genuinely need them, so whether or not they are “proper OOP” should be left to the theoreticians. Cleanup: finalization and garbage collection Programmers know about the importance of initialization, but often forget the importance of cleanup. After all, who needs to clean up an int? But with libraries, simply “letting go” of an object once you’re done with it is not always safe. Of course, Java has the garbage collector to reclaim the memory of objects that are no longer used. Now consider an unusual case: Suppose your object allocates “special” memory without using new. The garbage collector only knows how to release memory allocated with new, so it won’t know how to release the object’s “special” memory. To handle this case, Java provides a method called finalize( ) that you can define for your class. Here’s how it’s supposed to work. When the garbage collector is ready to release the storage used for your object, it will first call finalize( ), and only on the next garbage-collection pass will it reclaim the object’s memory. So if you choose to use finalize( ), it gives you the ability to perform some important cleanup at the time of garbage collection. This is a potential programming pitfall because some programmers, especially C++ programmers, might initially mistake finalize( ) for the destructor in C++, which is a function that is always called when an object is destroyed. It is important to distinguish between C++ and Java here, because in C++, objects always get destroyed (in a bug-free program), whereas in Java, objects do not always get garbage collected. Or, put another way: 1.Your objects might not get garbage collected. 2The one case in which this is possible occurs if you pass a reference to an object into the static method (the static method could also create its own object). Then, via the reference (which is now effectively this), you can call non-static methods and access non-static fields. But typically, if you want to do something like this, you’ll just make an ordinary, non-static method. 2.Garbage collection is not destruction. If you remember this, you will stay out of trouble. What it means is that if there is some activity that must be performed before you no longer need an object, you must perform that activity yourself. Java has no destructor or similar concept, so you must create an ordinary method to perform this cleanup. For example, suppose that in the process of creating your object, it draws itself on the screen. If you don’t explicitly erase its image from the screen, it might never get cleaned up. If you put some kind of erasing functionality inside finalize( ), then if an object is garbage collected and finalize( ) is called (and there’s no guarantee this will happen), then the image will first be removed from the screen, but if it isn’t, the image will remain. You might find that the storage for an object never gets released because your program never nears the point of running out of storage. If your program completes and the garbage collector never gets around to releasing the storage for any of your objects, that storage will be returned to the operating system en masse as the program exits. This is a good thing, because garbage collection has some overhead, and if you never do it, you never incur that expense.
## What is finalize() for?

<!--p143-->
So, if you should not use finalize( ) as a general-purpose cleanup method, what good is it? A third point to remember is: 3.Garbage collection is only about memory. That is, the sole reason for the existence of the garbage collector is to recover memory that your program is no longer using. So any activity that is associated with garbage collection, most notably your finalize( ) method, must also be only about memory and its deallocation. Does this mean that if your object contains other objects, finalize( ) should explicitly release those objects? Well, no—the garbage collector takes care of the release of all object memory regardless of how the object is created. It turns out that the need for finalize( ) is limited to special cases in which your object can allocate storage in some way other than creating an object. But, you might observe, everything in Java is an object, so how can this be? It would seem that finalize( ) is in place because of the possibility that you’ll do something Clike by allocating memory using a mechanism other than the normal one in Java. This can happen primarily through native methods, which are a way to call non-Java code from Java. (Native methods are covered in Appendix B in the electronic 2nd edition of this book, available at www.MindView.net.) C and C++ are the only languages currently supported by native methods, but since they can call subprograms in other languages, you can effectively call anything. Inside the non-Java code, C’s malloc( ) family of functions might be called to allocate storage, and unless you call free( ), that storage will not be released, causing a memory leak. Of course, free( ) is a C and C++ function, so you’d need to call it in a native method inside your finalize( ). After reading this, you probably get the idea that you won’t use finalize( ) much.3 You’re correct; it is not the appropriate place for normal cleanup to occur. So where should normal cleanup be performed? 3Joshua Bloch goes further in his section titled “avoid finalizers”: “Finalizers are unpredictable, often dangerous, and generally unnecessary.” Effective JavaTM Programming Language Guide, p. 20 (Addison-Wesley, 2001). Initialization & Cleanup You must perform cleanup To clean up an object, the user of that object must call a cleanup method at the point the cleanup is desired. This sounds pretty straightforward, but it collides a bit with the C++ concept of the destructor. In C++, all objects are destroyed. Or rather, all objects should be destroyed. If the C++ object is created as a local (i.e., on the stack—not possible in Java), then the destruction happens at the closing curly brace of the scope in which the object was created. If the object was created using new (like in Java), the destructor is called when the programmer calls the C++ operator delete (which doesn’t exist in Java). If the C++ programmer forgets to call delete, the destructor is never called, and you have a memory leak, plus the other parts of the object never get cleaned up. This kind of bug can be very difficult to track down, and is one of the compelling reasons to move from C++ to Java. In contrast, Java doesn’t allow you to create local objects—you must always use new. But in Java, there’s no “delete” for releasing the object, because the garbage collector releases the storage for you. So from a simplistic standpoint, you could say that because of garbage collection, Java has no destructor. You’ll see as this book progresses, however, that the presence of a garbage collector does not remove the need for or the utility of destructors. (And you should never call finalize( ) directly, so that’s not a solution.) If you want some kind of cleanup performed other than storage release, you must still explicitly call an appropriate method in Java, which is the equivalent of a C++ destructor without the convenience. Remember that neither garbage collection nor finalization is guaranteed. If the JVM isn’t close to running out of memory, then it might not waste time recovering memory through garbage collection. The termination condition In general, you can’t rely on finalize( ) being called, and you must create separate “cleanup” methods and call them explicitly. So it appears that finalize( ) is only useful for obscure memory cleanup that most programmers will never use. However, there is an interesting use of finalize( ) that does not rely on it being called every time. This is the verification of the termination condition4 of an object. At the point that you’re no longer interested in an object—when it’s ready to be cleaned up— that object should be in a state whereby its memory can be safely released. For example, if the object represents an open file, that file should be closed by the programmer before the object is garbage collected. If any portions of the object are not properly cleaned up, then you have a bug in your program that can be very difficult to find. finalize( ) can be used to eventually discover this condition, even if it isn’t always called. If one of the finalizations happens to reveal the bug, then you discover the problem, which is all you really care about. Here’s a simple example of how you might use it:
```java
//: initialization/TerminationCondition.java
// Using finalize() to detect an object that
// hasn’t been properly cleaned up.
class Book {
boolean checkedOut = false;
Book(boolean checkOut) {
checkedOut = checkOut;
}
```

<!--p144-->
4A term coined by Bill Venners (www.Artima.com) during a seminar that he and I were giving together.
```java
void checkIn() {
checkedOut = false;
}
protected void finalize() {
if(checkedOut)
System.out.println("Error: checked out");
// Normally, you’ll also do this:
// super.finalize(); // Call the base-class version
}
}
public class TerminationCondition {
public static void main(String[] args) {
Book novel = new Book(true);
// Proper cleanup:
novel.checkIn();
// Drop the reference, forget to clean up:
new Book(true);
// Force garbage collection & finalization:
System.gc();
}
} /* Output:
Error: checked out
*///:~
```

<!--p145-->

<!--p146-->

<!--p147-->
The termination condition is that all Book objects are supposed to be checked in before they are garbage collected, but in main( ), a programmer error doesn’t check in one of the books. Without finalize( ) to verify the termination condition, this can be a difficult bug to find. Note that System.gc( ) is used to force finalization. But even if it isn’t, it’s highly probable that the errant Book will eventually be discovered through repeated executions of the program (assuming the program allocates enough storage to cause the garbage collector to execute). You should generally assume that the base-class version of finalize( ) will also be doing something important, and call it using super, as you can see in Book.finalize( ). In this case, it is commented out because it requires exception handling, which we haven’t covered yet. Exercise 10:(2) Create a class with a finalize( ) method that prints a message. In main( ), create an object of your class. Explain the behavior of your program. Exercise 11:(4) Modify the previous exercise so that your finalize( ) will always be called. Exercise 12:(4) Create a class called Tank that can be filled and emptied, and has a termination condition that it must be empty when the object is cleaned up. Write a finalize( ) that verifies this termination condition. In main( ), test the possible scenarios that can occur when your Tank is used. How a garbage collector works If you come from a programming language where allocating objects on the heap is expensive, you may naturally assume that Java’s scheme of allocating everything (except primitives) on the heap is also expensive. However, it turns out that the garbage collector can have a significant impact on increasing the speed of object creation. This might sound a bit odd at first—that storage release affects storage allocation—but it’s the way some JVMs work, and it means that allocating storage for heap objects in Java can be nearly as fast as creating storage on the stack in other languages. For example, you can think of the C++ heap as a yard where each object stakes out its own piece of turf. This real estate can become abandoned sometime later and must be reused. In some JVMs, the Java heap is quite different; it’s more like a conveyor belt that moves forward every time you allocate a new object. This means that object storage allocation is remarkably rapid. The “heap pointer” is simply moved forward into virgin territory, so it’s effectively the same as C++’s stack allocation. (Of course, there’s a little extra overhead for bookkeeping, but it’s nothing like searching for storage.) You might observe that the heap isn’t in fact a conveyor belt, and if you treat it that way, you’ll start paging memory—moving it on and off disk, so that you can appear to have more memory than you actually do. Paging significantly impacts performance. Eventually, after you create enough objects, you’ll run out of memory. The trick is that the garbage collector steps in, and while it collects the garbage it compacts all the objects in the heap so that you’ve effectively moved the “heap pointer” closer to the beginning of the conveyor belt and farther away from a page fault. The garbage collector rearranges things and makes it possible for the high-speed, infinite-free-heap model to be used while allocating storage. To understand garbage collection in Java, it’s helpful learn how garbage-collection schemes work in other systems. A simple but slow garbage-collection technique is called reference counting. This means that each object contains a reference counter, and every time a reference is attached to that object, the reference count is increased. Every time a reference goes out of scope or is set to null, the reference count is decreased. Thus, managing reference counts is a small but constant overhead that happens throughout the lifetime of your program. The garbage collector moves through the entire list of objects, and when it finds one with a reference count of zero it releases that storage (however, reference counting schemes often release an object as soon as the count goes to zero). The one drawback is that if objects circularly refer to each other they can have nonzero reference counts while still being garbage. Locating such self-referential groups requires significant extra work for the garbage collector. Reference counting is commonly used to explain one kind of garbage collection, but it doesn’t seem to be used in any JVM implementations. In faster schemes, garbage collection is not based on reference counting. Instead, it is based on the idea that any non-dead object must ultimately be traceable back to a reference that lives either on the stack or in static storage. The chain might go through several layers of objects. Thus, if you start in the stack and in the static storage area and walk through all the references, you’ll find all the live objects. For each reference that you find, you must trace into the object that it points to and then follow all the references in that object, tracing into the objects they point to, etc., until you’ve moved through the entire Web that originated with the reference on the stack or in static storage. Each object that you move through must still be alive. Note that there is no problem with detached self-referential groups—these are simply not found, and are therefore automatically garbage. In the approach described here, the JVM uses an adaptive garbage-collection scheme, and what it does with the live objects that it locates depends on the variant currently being used. One of these variants is stop-and-copy. This means that—for reasons that will become apparent—the program is first stopped (this is not a background collection scheme). Then, each live object is copied from one heap to another, leaving behind all the garbage. In addition, as the objects are copied into the new heap, they are packed end-to-end, thus compacting the new heap (and allowing new storage to simply be reeled off the end as previously described). Of course, when an object is moved from one place to another, all references that point at the object must be changed. The reference that goes from the heap or the static storage area to the object can be changed right away, but there can be other references pointing to this object Initialization & Cleanup that will be encountered later during the “walk.” These are fixed up as they are found (you could imagine a table that maps old addresses to new ones). There are two issues that make these so-called “copy collectors” inefficient. The first is the idea that you have two heaps and you slosh all the memory back and forth between these two separate heaps, maintaining twice as much memory as you actually need. Some JVMs deal with this by allocating the heap in chunks as needed and simply copying from one chunk to another. The second issue is the copying process itself. Once your program becomes stable, it might be generating little or no garbage. Despite that, a copy collector will still copy all the memory from one place to another, which is wasteful. To prevent this, some JVMs detect that no new garbage is being generated and switch to a different scheme (this is the “adaptive” part). This other scheme is called mark-and-sweep, and it’s what earlier versions of Sun’s JVM used all the time. For general use, mark-and-sweep is fairly slow, but when you know you’re generating little or no garbage, it’s fast. Mark-and-sweep follows the same logic of starting from the stack and static storage, and tracing through all the references to find live objects. However, each time it finds a live object, that object is marked by setting a flag in it, but the object isn’t collected yet. Only when the marking process is finished does the sweep occur. During the sweep, the dead objects are released. However, no copying happens, so if the collector chooses to compact a fragmented heap, it does so by shuffling objects around. “Stop-and-copy” refers to the idea that this type of garbage collection is not done in the background; instead, the program is stopped while the garbage collection occurs. In the Sun literature you’ll find many references to garbage collection as a low-priority background process, but it turns out that the garbage collection was not implemented that way in earlier versions of the Sun JVM. Instead, the Sun garbage collector stopped the program when memory got low. Mark-and-sweep also requires that the program be stopped. As previously mentioned, in the JVM described here memory is allocated in big blocks. If you allocate a large object, it gets its own block. Strict stop-and-copy requires copying every live object from the source heap to a new heap before you can free the old one, which translates to lots of memory. With blocks, the garbage collection can typically copy objects to dead blocks as it collects. Each block has a generation count to keep track of whether it’s alive. In the normal case, only the blocks created since the last garbage collection are compacted; all other blocks get their generation count bumped if they have been referenced from somewhere. This handles the normal case of lots of short-lived temporary objects. Periodically, a full sweep is made—large objects are still not copied (they just get their generation count bumped), and blocks containing small objects are copied and compacted. The JVM monitors the efficiency of garbage collection and if it becomes a waste of time because all objects are long-lived, then it switches to mark-andsweep. Similarly, the JVM keeps track of how successful mark-and-sweep is, and if the heap starts to become fragmented, it switches back to stop-and-copy. This is where the “adaptive” part comes in, so you end up with a mouthful: “Adaptive generational stop-and-copy mark-andsweep.” There are a number of additional speedups possible in a JVM. An especially important one involves the operation of the loader and what is called a just-in-time (JIT) compiler. A JIT compiler partially or fully converts a program into native machine code so that it doesn’t need to be interpreted by the JVM and thus runs much faster. When a class must be loaded (typically, the first time you want to create an object of that class), the .class file is located, and the bytecodes for that class are brought into memory. At this point, one approach is to simply JIT compile all the code, but this has two drawbacks: It takes a little more time, which, compounded throughout the life of the program, can add up; and it increases the size of the executable (bytecodes are significantly more compact than expanded JIT code), and this might cause paging, which definitely slows down a program. An alternative approach is lazy evaluation, which means that the code is not JIT compiled until necessary. Thus, code that never gets executed might never be JIT compiled. The Java HotSpot technologies in recent JDKs take a similar approach by increasingly optimizing a piece of code each time it is executed, so the more the code is executed, the faster it gets. Member initialization Java goes out of its way to guarantee that variables are properly initialized before they are used. In the case of a method’s local variables, this guarantee comes in the form of a compile- time error. So if you say:
```java
void f() {
int i;
i++; // Error -- i not initialized
}
```
you’ll get an error message that says that i might not have been initialized. Of course, the compiler could have given i a default value, but an uninitialized local variable is probably a programmer error, and a default value would have covered that up. Forcing the programmer to provide an initialization value is more likely to catch a bug. If a primitive is a field in a class, however, things are a bit different. As you saw in the Everything Is an Object chapter, each primitive field of a class is guaranteed to get an initial value. Here’s a program that verifies this, and shows the values:
```java
//: initialization/InitialValues.java
// Shows default initial values.
import static net.mindview.util.Print.*;
public class InitialValues {
boolean t;
char c;
byte b;
short s;
int i;
long l;
float f;
double d;
InitialValues reference;
void printInitialValues() {
print("Data type Initial value");
print("boolean " + t);
print("char [" + c + "]");
print("byte " + b);
print("short " + s);
print("int " + i);
print("long " + l);
print("float " + f);
print("double " + d);
print("reference " + reference);
}
public static void main(String[] args) {
InitialValues iv = new InitialValues();
iv.printInitialValues();
/* You could also say:
new InitialValues().printInitialValues();
*/
}
} /* Output:
Data type Initial value
```

<!--p148-->
Initialization & Cleanup
```java
boolean false
char [ ]
byte 0
short 0
int 0
long 0
float 0.0
double 0.0
reference null
*///:~
```
You can see that even though the values are not specified, they automatically get initialized (the char value is a zero, which prints as a space). So at least there’s no threat of working with uninitialized variables. When you define an object reference inside a class without initializing it to a new object, that reference is given a special value of null. Specifying initialization What happens if you want to give a variable an initial value? One direct way to do this is simply to assign the value at the point you define the variable in the class. (Notice you cannot do this in C++, although C++ novices always try.) Here the field definitions in class InitialValues are changed to provide initial values:
```java
//: initialization/InitialValues2.java
// Providing explicit initial values.
public class InitialValues2 {
boolean bool = true;
char ch = ‘x’;
byte b = 47;
short s = 0xff;
int i = 999;
long lng = 1;
float f = 3.14f;
double d = 3.14159;
} ///:~
```
You can also initialize non-primitive objects in this same way. If Depth is a class, you can create a variable and initialize it like so:
```java
//: initialization/Measurement.java
class Depth {}
public class Measurement {
Depth d = new Depth();
// ...
} ///:~
```
If you haven’t given d an initial value and you try to use it anyway, you’ll get a runtime error called an exception (covered in the Error Handling with Exceptions chapter). You can even call a method to provide an initialization value:

<!--p149-->
```java
//: initialization/MethodInit.java
public class MethodInit {
int i = f();
int f() { return 11; }
} ///:~
```
This method can have arguments, of course, but those arguments cannot be other class members that haven’t been initialized yet. Thus, you can do this:
```java
//: initialization/MethodInit2.java
public class MethodInit2 {
int i = f();
int j = g(i);
int f() { return 11; }
int g(int n) { return n * 10; }
} ///:~
```
But you cannot do this:
```java
//: initialization/MethodInit3.java
public class MethodInit3 {
//! int j = g(i); // Illegal forward reference
int i = f();
int f() { return 11; }
int g(int n) { return n * 10; }
} ///:~
```
This is one place in which the compiler, appropriately, does complain about forward referencing, since this has to do with the order of initialization and not the way the program is compiled. This approach to initialization is simple and straightforward. It has the limitation that every object of type InitialValues will get these same initialization values. Sometimes this is exactly what you need, but at other times you need more flexibility. Constructor initialization The constructor can be used to perform initialization, and this gives you greater flexibility in your programming because you can call methods and perform actions at run time to determine the initial values. There’s one thing to keep in mind, however: You aren’t precluding the automatic initialization, which happens before the constructor is entered. So, for example, if you say:
```java
//: initialization/Counter.java
public class Counter {
int i;
Counter() { i = 7; }
// ...
} ///:~
```

<!--p150-->
then i will first be initialized to 0, then to 7. This is true with all the primitive types and with object references, including those that are given explicit initialization at the point of definition. For this reason, the compiler doesn’t try to force you to initialize elements in the constructor at any particular place, or before they are used—initialization is already guaranteed. Order of initialization Within a class, the order of initialization is determined by the order that the variables are defined within the class. The variable definitions may be scattered throughout and in Initialization & Cleanup between method definitions, but the variables are initialized before any methods can be called—even the constructor. For example:
```java
//: initialization/OrderOfInitialization.java
// Demonstrates initialization order.
import static net.mindview.util.Print.*;
// When the constructor is called to create a
// Window object, you’ll see a message:
class Window {
Window(int marker) { print("Window(" + marker + ")"); }
}
class House {
Window w1 = new Window(1); // Before constructor
House() {
// Show that we’re in the constructor:
print("House()");
w3 = new Window(33); // Reinitialize w3
}
Window w2 = new Window(2); // After constructor
void f() { print("f()"); }
Window w3 = new Window(3); // At end
}
public class OrderOfInitialization {
public static void main(String[] args) {
House h = new House();
h.f(); // Shows that construction is done
}
} /* Output:
Window(1)
Window(2)
Window(3)
House()
Window(33)
f()
*///:~
```
In House, the definitions of the Window objects are intentionally scattered about to prove that they’ll all get initialized before the constructor is entered or anything else can happen. In addition, w3 is reinitialized inside the constructor. From the output, you can see that the w3 reference gets initialized twice: once before and once during the constructor call. (The first object is dropped, so it can be garbage collected later.) This might not seem efficient at first, but it guarantees proper initialization—what would happen if an overloaded constructor were defined that did not initialize w3 and there wasn’t a “default” initialization for w3 in its definition?
## static data initialization

<!--p151-->
There’s only a single piece of storage for a static, regardless of how many objects are created. You can’t apply the static keyword to local variables, so it only applies to fields. If a field is a static primitive and you don’t initialize it, it gets the standard initial value for its type. If it’s a reference to an object, the default initialization value is null. If you want to place initialization at the point of definition, it looks the same as for non- statics. To see when the static storage gets initialized, here’s an example:
```java
//: initialization/StaticInitialization.java
// Specifying initial values in a class definition.
import static net.mindview.util.Print.*;
class Bowl {
Bowl(int marker) {
print("Bowl(" + marker + ")");
}
void f1(int marker) {
print("f1(" + marker + ")");
}
}
class Table {
static Bowl bowl1 = new Bowl(1);
Table() {
print("Table()");
bowl2.f1(1);
}
void f2(int marker) {
print("f2(" + marker + ")");
}
static Bowl bowl2 = new Bowl(2);
}
class Cupboard {
Bowl bowl3 = new Bowl(3);
static Bowl bowl4 = new Bowl(4);
Cupboard() {
print("Cupboard()");
bowl4.f1(2);
}
void f3(int marker) {
print("f3(" + marker + ")");
}
static Bowl bowl5 = new Bowl(5);
}
public class StaticInitialization {
public static void main(String[] args) {
print("Creating new Cupboard() in main");
new Cupboard();
print("Creating new Cupboard() in main");
new Cupboard();
table.f2(1);
cupboard.f3(1);
}
static Table table = new Table();
static Cupboard cupboard = new Cupboard();
} /* Output:
Bowl(1)
Bowl(2)
Table()
f1(1)
Bowl(4)
Bowl(5)
Bowl(3)
Cupboard()
f1(2)
Creating new Cupboard() in main
Bowl(3)
```

<!--p152-->
Initialization & Cleanup
```java
Cupboard()
f1(2)
Creating new Cupboard() in main
Bowl(3)
Cupboard()
f1(2)
f2(1)
f3(1)
*///:~
```
Bowl allows you to view the creation of a class, and Table and Cupboard have static members of Bowl scattered through their class definitions. Note that Cupboard creates a non-static Bowl bowl3 prior to the static definitions. From the output, you can see that the static initialization occurs only if it’s necessary. If you don’t create a Table object and you never refer to Table.bowl1 or Table.bowl2, the static Bowl bowl1 and bowl2 will never be created. They are initialized only when the first Table object is created (or the first static access occurs). After that, the static objects are not reinitialized. The order of initialization is statics first, if they haven’t already been initialized by a previous object creation, and then the non-static objects. You can see the evidence of this in the output. To execute main( ) (a static method), the StaticInitialization class must be loaded, and its static fields table and cupboard are then initialized, which causes those classes to be loaded, and since they both contain static Bowl objects, Bowl is then loaded. Thus, all the classes in this particular program get loaded before main( ) starts. This is usually not the case, because in typical programs you won’t have everything linked together by statics as you do in this example. To summarize the process of creating an object, consider a class called Dog: 1.Even though it doesn’t explicitly use the static keyword, the constructor is actually a static method. So the first time an object of type Dog is created, or the first time a static method or static field of class Dog is accessed, the Java interpreter must locate Dog.class, which it does by searching through the classpath. 2.As Dog.class is loaded (creating a Class object, which you’ll learn about later), all of its static initializers are run. Thus, static initialization takes place only once, as the Class object is loaded for the first time. 3.When you create a new Dog( ), the construction process for a Dog object first allocates enough storage for a Dog object on the heap. 4.This storage is wiped to zero, automatically setting all the primitives in that Dog object to their default values (zero for numbers and the equivalent for boolean and char) and the references to null. 5.Any initializations that occur at the point of field definition are executed. 6.Constructors are executed. As you shall see in the Reusing Classes chapter, this might actually involve a fair amount of activity, especially when inheritance is involved.
## Explicit static initialization

<!--p153-->
Java allows you to group other static initializations inside a special “static clause” (sometimes called a static block) in a class. It looks like this:
```java
//: initialization/Spoon.java
public class Spoon {
static int i;
static {
i = 47;
}
} ///:~
```
It appears to be a method, but it’s just the static keyword followed by a block of code. This code, like other static initializations, is executed only once: the first time you make an object of that class or the first time you access a static member of that class (even if you never make an object of that class). For example:
```java
//: initialization/ExplicitStatic.java
// Explicit static initialization with the "static" clause.
import static net.mindview.util.Print.*;
class Cup {
Cup(int marker) {
print("Cup(" + marker + ")");
}
void f(int marker) {
print("f(" + marker + ")");
}
}
class Cups {
static Cup cup1;
static Cup cup2;
static {
cup1 = new Cup(1);
cup2 = new Cup(2);
}
Cups() {
print("Cups()");
}
}
public class ExplicitStatic {
public static void main(String[] args) {
print("Inside main()");
Cups.cup1.f(99); // (1)
}
// static Cups cups1 = new Cups(); // (2)
// static Cups cups2 = new Cups(); // (2)
} /* Output:
Inside main()
Cup(1)
Cup(2)
f(99)
*///:~
```

<!--p154-->
The static initializers for Cups run when either the access of the static object cup1 occurs on the line marked (1), or if line (1) is commented out and the lines marked (2) are uncommented. If both (1) and (2) are commented out, the static initialization for Cups never occurs, as you can see from the output. Also, it doesn’t matter if one or both of the lines marked (2) are uncommented; the static initialization only occurs once. Exercise 13:(1) Verify the statements in the previous paragraph. Initialization & Cleanup Exercise 14:(1) Create a class with a static String field that is initialized at the point of definition, and another one that is initialized by the static block. Add a static method that prints both fields and demonstrates that they are both initialized before they are used.
## Non-static instance initialization
Java provides a similar syntax, called instance initialization, for initializing non-static variables for each object. Here’s an example:
```java
//: initialization/Mugs.java
// Java "Instance Initialization."
import static net.mindview.util.Print.*;
class Mug {
Mug(int marker) {
print("Mug(" + marker + ")");
}
void f(int marker) {
print("f(" + marker + ")");
}
}
public class Mugs {
Mug mug1;
Mug mug2;
{
mug1 = new Mug(1);
mug2 = new Mug(2);
print("mug1 & mug2 initialized");
}
Mugs() {
print("Mugs()");
}
Mugs(int i) {
print("Mugs(int)");
}
public static void main(String[] args) {
print("Inside main()");
new Mugs();
print("new Mugs() completed");
new Mugs(1);
print("new Mugs(1) completed");
}
} /* Output:
Inside main()
Mug(1)
Mug(2)
mug1 & mug2 initialized
Mugs()
new Mugs() completed
Mug(1)
Mug(2)
mug1 & mug2 initialized
Mugs(int)
new Mugs(1) completed
*///:~
```
You can see that the instance initialization clause:

<!--p155-->
```java
{
mug1 = new Mug(1);
mug2 = new Mug(2);
print("mug1 & mug2 initialized");
}
```
looks exactly like the static initialization clause except for the missing static keyword. This syntax is necessary to support the initialization of anonymous inner classes (see the Inner Classes chapter), but it also allows you to guarantee that certain operations occur regardless of which explicit constructor is called. From the output, you can see that the instance initialization clause is executed before either one of the constructors. Exercise 15:(1) Create a class with a String that is initialized using instance initialization. Array initialization An array is simply a sequence of either objects or primitives that are all the same type and are packaged together under one identifier name. Arrays are defined and used with the square- brackets indexing operator [ ]. To define an array reference, you simply follow your type name with empty square brackets:
```java
int[] a1;
```
You can also put the square brackets after the identifier to produce exactly the same meaning:
```java
int a1[];
```
This conforms to expectations from C and C++ programmers. The former style, however, is probably a more sensible syntax, since it says that the type is “an int array.” That style will be used in this book. The compiler doesn’t allow you to tell it how big the array is. This brings us back to that issue of “references.” All that you have at this point is a reference to an array (you’ve allocated enough storage for that reference), and there’s been no space allocated for the array object itself. To create storage for the array, you must write an initialization expression. For arrays, initialization can appear anywhere in your code, but you can also use a special kind of initialization expression that must occur at the point where the array is created. This special initialization is a set of values surrounded by curly braces. The storage allocation (the equivalent of using new) is taken care of by the compiler in this case. For example:
```java
int[] a1 = { 1, 2, 3, 4, 5 };
```
So why would you ever define an array reference without an array?
```java
int[] a2;
```
Well, it’s possible to assign one array to another in Java, so you can say:
```java
a2 = a1;
```
What you’re really doing is copying a reference, as demonstrated here:
```java
//: initialization/ArraysOfPrimitives.java
import static net.mindview.util.Print.*;
```

<!--p156-->
Initialization & Cleanup
```java
public class ArraysOfPrimitives {
public static void main(String[] args) {
int[] a1 = { 1, 2, 3, 4, 5 };
int[] a2;
a2 = a1;
for(int i = 0; i < a2.length; i++)
a2[i] = a2[i] + 1;
for(int i = 0; i < a1.length; i++)
print("a1[" + i + "] = " + a1[i]);
}
} /* Output:
a1[0] = 2
a1[1] = 3
a1[2] = 4
a1[3] = 5
a1[4] = 6
*///:~
```
You can see that a1 is given an initialization value but a2 is not; a2 is assigned later—in this case, to another array. Since a2 and a1 are then aliased to the same array, the changes made via a2 are seen in a1. All arrays have an intrinsic member (whether they’re arrays of objects or arrays of primitives) that you can query—but not change—to tell you how many elements there are in the array. This member is length. Since arrays in Java, like C and C++, start counting from element zero, the largest element you can index is length - 1. If you go out of bounds, C and C++ quietly accept this and allow you to stomp all over your memory, which is the source of many infamous bugs. However, Java protects you against such problems by causing a runtime error (an exception) if you step out of bounds.5 What if you don’t know how many elements you’re going to need in your array while you’re writing the program? You simply use new to create the elements in the array. Here, new works even though it’s creating an array of primitives (new won’t create a non-array primitive):
```java
//: initialization/ArrayNew.java
// Creating arrays with new.
import java.util.*;
import static net.mindview.util.Print.*;
public class ArrayNew {
public static void main(String[] args) {
int[] a;
Random rand = new Random(47);
a = new int[rand.nextInt(20)];
print("length of a = " + a.length);
print(Arrays.toString(a));
}
} /* Output:
length of a = 18
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
*///:~
```

<!--p157-->
The size of the array is chosen at random by using the Random.nextInt( ) method, which produces a value between zero and that of its argument. Because of the randomness, it’s clear 5Of course, checking every array access costs time and code and there’s no way to turn it off, which means that array accesses might be a source of inefficiency in your program if they occur at a critical juncture. For Internet security and programmer productivity, the Java designers saw that this was a worthwhile trade-off. Although you may be tempted to write code that you think might make array accesses more efficient, this is a waste of time because automatic compile-time and runtime optimizations will speed array accesses. that array creation is actually happening at run time. In addition, the output of this program shows that array elements of primitive types are automatically initialized to “empty” values. (For numerics and char, this is zero, and for boolean, it’s false.) The Arrays.toString( ) method, which is part of the standard java.util library, produces a printable version of a one-dimensional array. Of course, in this case the array could also have been defined and initialized in the same statement:
```java
int[] a = new int[rand.nextInt(20)];
```
This is the preferred way to do it, if you can. If you create a non-primitive array, you create an array of references. Consider the wrapper type Integer, which is a class and not a primitive:
```java
//: initialization/ArrayClassObj.java
// Creating an array of nonprimitive objects.
import java.util.*;
import static net.mindview.util.Print.*;
public class ArrayClassObj {
public static void main(String[] args) {
Random rand = new Random(47);
Integer[] a = new Integer[rand.nextInt(20)];
print("length of a = " + a.length);
for(int i = 0; i < a.length; i++)
a[i] = rand.nextInt(500); // Autoboxing
print(Arrays.toString(a));
}
} /* Output: (Sample)
length of a = 18
[55, 193, 361, 461, 429, 368, 200, 22, 207, 288, 128, 51, 89, 309, 278,
498, 361, 20]
*///:~
```
Here, even after new is called to create the array:
```java
Integer[] a = new Integer[rand.nextInt(20)];
```
it’s only an array of references, and the initialization is not complete until the reference itself is initialized by creating a new Integer object (via autoboxing, in this case):
```java
a[i] = rand.nextInt(500);
```
If you forget to create the object, however, you’ll get an exception at run time when you try to use the empty array location. It’s also possible to initialize arrays of objects by using the curly brace-enclosed list. There are two forms:
```java
//: initialization/ArrayInit.java
// Array initialization.
import java.util.*;
public class ArrayInit {
public static void main(String[] args) {
Integer[] a = {
```

<!--p158-->
Initialization & Cleanup
```java
new Integer(1),
new Integer(2),
3, // Autoboxing
};
Integer[] b = new Integer[]{
new Integer(1),
new Integer(2),
3, // Autoboxing
};
System.out.println(Arrays.toString(a));
System.out.println(Arrays.toString(b));
}
} /* Output:
[1, 2, 3]
[1, 2, 3]
*///:~
```
In both cases, the final comma in the list of initializers is optional. (This feature makes for easier maintenance of long lists.) Although the first form is useful, it’s more limited because it can only be used at the point where the array is defined. You can use the second and third forms anywhere, even inside a method call. For example, you could create an array of String objects to pass to the main( ) of another method, to provide alternate command-line arguments to that main( ):
```java
//: initialization/DynamicArray.java
// Array initialization.
public class DynamicArray {
public static void main(String[] args) {
Other.main(new String[]{ "fiddle", "de", "dum" });
}
}
class Other {
public static void main(String[] args) {
for(String s : args)
System.out.print(s + " ");
}
} /* Output:
fiddle de dum
*///:~
```

<!--p159-->
The array created for the argument of Other.main( ) is created at the point of the method call, so you can even provide alternate arguments at the time of the call. Exercise 16:(1) Create an array of String objects and assign a String to each element. Print the array by using a for loop. Exercise 17:(2) Create a class with a constructor that takes a String argument. During construction, print the argument. Create an array of object references to this class, but don’t actually create objects to assign into the array. When you run the program, notice whether the initialization messages from the constructor calls are printed. Exercise 18:(1) Complete the previous exercise by creating objects to attach to the array of references. Variable argument lists The second form provides a convenient syntax to create and call methods that can produce an effect similar to C’s variable argument lists (known as “varargs” in C). These can include unknown quantities of arguments as well as unknown types. Since all classes are ultimately inherited from the common root class Object (a subject you will learn more about as this book progresses), you can create a method that takes an array of Object and call it like this:
```java
//: initialization/VarArgs.java
// Using array syntax to create variable argument lists.
class A {}
public class VarArgs {
static void printArray(Object[] args) {
for(Object obj : args)
System.out.print(obj + " ");
System.out.println();
}
public static void main(String[] args) {
printArray(new Object[]{
new Integer(47), new Float(3.14), new Double(11.11)
});
printArray(new Object[]{"one", "two", "three" });
printArray(new Object[]{new A(), new A(), new A()});
}
} /* Output: (Sample)
47 3.14 11.11
one two three
A@1a46e30 A@3e25a5 A@19821f
*///:~
```
You can see that print( ) takes an array of Object, then steps through the array using the foreach syntax and prints each one. The standard Java library classes produce sensible output, but the objects of the classes created here print the class name, followed by an ‘@’ sign and hexadecimal digits. Thus, the default behavior (if you don’t define a toString( ) method for your class, which will be described later in the book) is to print the class name and the address of the object. You may see pre-Java SE5 code written like the above in order to produce variable argument lists. In Java SE5, however, this long-requested feature was finally added, so you can now use ellipses to define a variable argument list, as you can see in printArray( ):
```java
//: initialization/NewVarArgs.java
// Using array syntax to create variable argument lists.
public class NewVarArgs {
static void printArray(Object... args) {
for(Object obj : args)
System.out.print(obj + " ");
System.out.println();
}
public static void main(String[] args) {
// Can take individual elements:
printArray(new Integer(47), new Float(3.14),
new Double(11.11));
printArray(47, 3.14F, 11.11);
printArray("one", "two", "three");
printArray(new A(), new A(), new A());
// Or an array:
```

<!--p160-->
Initialization & Cleanup
```java
printArray((Object[])new Integer[]{ 1, 2, 3, 4 });
printArray(); // Empty list is OK
}
} /* Output: (75% match)
47 3.14 11.11
47 3.14 11.11
one two three
A@1bab50a A@c3c749 A@150bd4d
1 2 3 4
*///:~
```
With varargs, you no longer have to explicitly write out the array syntax—the compiler will actually fill it in for you when you specify varargs. You’re still getting an array, which is why print( ) is able to use foreach to iterate through the array. However, it’s more than just an automatic conversion from a list of elements to an array. Notice the second-t0-last line in the program, where an array of Integer (created using autoboxing) is cast to an Object array (to remove a compiler warning) and passed to printArray( ). Clearly, the compiler sees that this is already an array and performs no conversion on it. So if you have a group of items you can pass them in as a list, and if you already have an array it will accept that as the variable argument list. The last line of the program shows that it’s possible to pass zero arguments to a vararg list. This is helpful when you have optional trailing arguments:
```java
//: initialization/OptionalTrailingArguments.java
public class OptionalTrailingArguments {
static void f(int required, String... trailing) {
System.out.print("required: " + required + " ");
for(String s : trailing)
System.out.print(s + " ");
System.out.println();
}
public static void main(String[] args) {
f(1, "one");
f(2, "two", "three");
f(0);
}
} /* Output:
required: 1 one
required: 2 two three
required: 0
*///:~
```
This also shows how you can use varargs with a specified type other than Object. Here, all the varargs must be String objects. It’s possible to use any type of argument in varargs, including a primitive type. The following example also shows that the vararg list becomes an array, and if there’s nothing in the list it’s an array of size zero:

<!--p161-->
```java
//: initialization/VarargType.java
public class VarargType {
static void f(Character... args) {
System.out.print(args.getClass());
System.out.println(" length " + args.length);
}
static void g(int... args) {
System.out.print(args.getClass());
System.out.println(" length " + args.length);
}
public static void main(String[] args) {
f(‘a’);
f();
g(1);
g();
System.out.println("int[]: " + new int[0].getClass());
}
} /* Output:
class [Ljava.lang.Character; length 1
class [Ljava.lang.Character; length 0
class [I length 1
class [I length 0
int[]: class [I
*///:~
```
The getClass( ) method is part of Object, and will be explored fully in the Type Information chapter. It produces the class of an object, and when you print this class, you see an encoded string representing the class type. The leading ‘[‘ indicates that this is an array of the type that follows. The ‘I’ is for a primitive int; to double-check, I created an array of int in the last line and printed its type. This verifies that using varargs does not depend on autoboxing, but that it actually uses the primitive types. Varargs do work in harmony with autoboxing, however. For example:
```java
//: initialization/AutoboxingVarargs.java
public class AutoboxingVarargs {
public static void f(Integer... args) {
for(Integer i : args)
System.out.print(i + " ");
System.out.println();
}
public static void main(String[] args) {
f(new Integer(1), new Integer(2));
f(4, 5, 6, 7, 8, 9);
f(10, new Integer(11), 12);
}
} /* Output:
1 2
4 5 6 7 8 9
10 11 12
*///:~
```
Notice that you can mix the types together in a single argument list, and autoboxing selectively promotes the int arguments to Integer. Varargs complicate the process of overloading, although it seems safe enough at first:
```java
//: initialization/OverloadingVarargs.java
public class OverloadingVarargs {
static void f(Character... args) {
System.out.print("first");
for(Character c : args)
System.out.print(" " + c);
System.out.println();
}
static void f(Integer... args) {
System.out.print("second");
for(Integer i : args)
System.out.print(" " + i);
System.out.println();
```

<!--p162-->
Initialization & Cleanup
```java
}
static void f(Long... args) {
System.out.println("third");
}
public static void main(String[] args) {
f(‘a’, ‘b’, ‘c’);
f(1);
f(2, 1);
f(0);
f(0L);
//! f(); // Won’t compile -- ambiguous
}
} /* Output:
first a b c
second 1
second 2 1
second 0
third
*///:~
```
In each case, the compiler is using autoboxing to match the overloaded method, and it calls the most specifically matching method. But when you call f( ) without arguments, it has no way of knowing which one to call. Although this error is understandable, it will probably surprise the client programmer. You might try solving the problem by adding a non-vararg argument to one of the methods:
```java
//: initialization/OverloadingVarargs2.java
// {CompileTimeError} (Won’t compile)
public class OverloadingVarargs2 {
static void f(float i, Character... args) {
System.out.println("first");
}
static void f(Character... args) {
System.out.print("second");
}
public static void main(String[] args) {
f(1, ‘a’);
f(‘a’, ‘b’);
}
} ///:~
```
The {CompileTimeError} comment tag excludes the file from this book’s Ant build. If you compile it by hand you’ll see the error message: reference to f is ambiguous, both method f(float,java.lang.Character...) in OverloadingVarargs2 and method f(java.lang.Character...) in OverloadingVarargs2 match If you give both methods a non-vararg argument, it works:

<!--p163-->
```java
//: initialization/OverloadingVarargs3.java
public class OverloadingVarargs3 {
static void f(float i, Character... args) {
System.out.println("first");
}
static void f(char c, Character... args) {
System.out.println("second");
}
public static void main(String[] args) {
f(1, ‘a’);
f(‘a’, ‘b’);
}
} /* Output:
first
second
*///:~
```
You should generally only use a variable argument list on one version of an overloaded method. Or consider not doing it at all. Exercise 19:(2) Write a method that takes a vararg String array. Verify that you can pass either a comma-separated list of Strings or a String[] into this method. Exercise 20:(1) Create a main( ) that uses varargs instead of the ordinary main( ) syntax. Print all the elements in the resulting args array. Test it with various numbers of command-line arguments. Enumerated types An apparently small addition in Java SE5 is the enum keyword, which makes your life much easier when you need to group together and use a set of enumerated types. In the past you would have created a set of constant integral values, but these do not naturally restrict themselves to your set and thus are riskier and more difficult to use. Enumerated types are a common enough need that C, C++, and a number of other languages have always had them. Before Java SE5, Java programmers were forced to know a lot and be quite careful when they wanted to properly produce the enum effect. Now Java has enum, too, and it’s much more full-featured than what you find in C/C++. Here’s a simple example:
```java
//: initialization/Spiciness.java
public enum Spiciness {
NOT, MILD, MEDIUM, HOT, FLAMING
} ///:~
```
This creates an enumerated type called Spiciness with five named values. Because the instances of enumerated types are constants, they are in all capital letters by convention (if there are multiple words in a name, they are separated by underscores). To use an enum, you create a reference of that type and assign it to an instance:
```java
//: initialization/SimpleEnumUse.java
public class SimpleEnumUse {
public static void main(String[] args) {
Spiciness howHot = Spiciness.MEDIUM;
System.out.println(howHot);
}
} /* Output:
MEDIUM
*///:~
```

<!--p164-->
The compiler automatically adds useful features when you create an enum. For example, it creates a toString( ) so that you can easily display the name of an enum instance, which is how the print statement above produced its output. The compiler also creates an ordinal( ) Initialization & Cleanup method to indicate the declaration order of a particular enum constant, and a static values( ) method that produces an array of values of the enum constants in the order that they were declared:
```java
//: initialization/EnumOrder.java
public class EnumOrder {
public static void main(String[] args) {
for(Spiciness s : Spiciness.values())
System.out.println(s + ", ordinal " + s.ordinal());
}
} /* Output:
NOT, ordinal 0
MILD, ordinal 1
MEDIUM, ordinal 2
HOT, ordinal 3
FLAMING, ordinal 4
*///:~
```
Although enums appear to be a new data type, the keyword only produces some compiler behavior while generating a class for the enum, so in many ways you can treat an enum as if it were any other class. In fact, enums are classes and have their own methods. An especially nice feature is the way that enums can be used inside switch statements:
```java
//: initialization/Burrito.java
public class Burrito {
Spiciness degree;
public Burrito(Spiciness degree) { this.degree = degree;}
public void describe() {
System.out.print("This burrito is ");
switch(degree) {
case NOT: System.out.println("not spicy at all.");
break;
case MILD:
case MEDIUM: System.out.println("a little hot.");
break;
case HOT:
case FLAMING:
default: System.out.println("maybe too hot.");
}
}
public static void main(String[] args) {
Burrito
plain = new Burrito(Spiciness.NOT),
greenChile = new Burrito(Spiciness.MEDIUM),
jalapeno = new Burrito(Spiciness.HOT);
plain.describe();
greenChile.describe();
jalapeno.describe();
}
} /* Output:
This burrito is not spicy at all.
This burrito is a little hot.
This burrito is maybe too hot.
*///:~
```

<!--p165-->
Since a switch is intended to select from a limited set of possibilities, it’s an ideal match for an enum. Notice how the enum names can produce a much clearer indication of what the program means to do. Initialization & Cleanup In general you can use an enum as if it were another way to create a data type, and then just put the results to work. That’s the point, so you don’t have to think too hard about them. Before the introduction of enum in Java SE5, you had to go to a lot of effort to make an equivalent enumerated type that was safe to use. This is enough for you to understand and use basic enums, but we’ll look more deeply at them later in the book—they have their own chapter: Enumerated Types. Exercise 21:(1) Create an enum of the least-valuable six types of paper currency. Loop through the values( ) and print each value and its ordinal( ). Exercise 22:(2) Write a switch statement for the enum in the previous example. For each case, output a description of that particular currency. Summary This seemingly elaborate mechanism for initialization, the constructor, should give you a strong hint about the critical importance placed on initialization in the language. As Bjarne Stroustrup, the inventor of C++, was designing that language, one of the first observations he made about productivity in C was that improper initialization of variables causes a significant portion of programming problems. These kinds of bugs are hard to find, and similar issues apply to improper cleanup. Because constructors allow you to guarantee proper initialization and cleanup (the compiler will not allow an object to be created without the proper constructor calls), you get complete control and safety. In C++, destruction is quite important because objects created with new must be explicitly destroyed. In Java, the garbage collector automatically releases the memory for all objects, so the equivalent cleanup method in Java isn’t necessary much of the time (but when it is, you must do it yourself). In cases where you don’t need destructor-like behavior, Java’s garbage collector greatly simplifies programming and adds much-needed safety in managing memory. Some garbage collectors can even clean up other resources like graphics and file handles. However, the garbage collector does add a runtime cost, the expense of which is difficult to put into perspective because of the historical slowness of Java interpreters. Although Java has had significant performance increases over time, the speed problem has taken its toll on the adoption of the language for certain types of programming problems. Because of the guarantee that all objects will be constructed, there’s actually more to the constructor than what is shown here. In particular, when you create new classes using either composition or inheritance, the guarantee of construction also holds, and some additional syntax is necessary to support this. You’ll learn about composition, inheritance, and how they affect constructors in future chapters. Solutions to selected exercises can be found in the electronic document The Thinking in Java Annotated Solution Guide, available for sale from www.MindView.net.