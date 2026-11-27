# 7. Reusing Classes (printed p165-192)


<!--p187-->
Reusing Classes One of the most compelling features about Java is code reuse. But to be revolutionary, you’ve got to be able to do a lot more than copy code and change it. That’s the approach used in procedural languages like C, and it hasn’t worked very well. Like everything in Java, the solution revolves around the class. You reuse code by creating new classes, but instead of creating them from scratch, you use existing classes that someone has already built and debugged. The trick is to use the classes without soiling the existing code. In this chapter you’ll see two ways to accomplish this. The first is quite straightforward: you simply create objects of your existing class inside the new class. This is called composition, because the new class is composed of objects of existing classes. You’re simply reusing the functionality of the code, not its form. The second approach is more subtle. It creates a new class as a type of an existing class. You literally take the form of the existing class and add code to it without modifying the existing class. This technique is called inheritance, and the compiler does most of the work. Inheritance is one of the cornerstones of object-oriented programming, and has additional implications that will be explored in the Polymorphism chapter. It turns out that much of the syntax and behavior are similar for both composition and inheritance (which makes sense because they are both ways of making new types from existing types). In this chapter, you’ll learn about these code reuse mechanisms. Composition syntax Composition has been used quite frequently up to this point in the book. You simply place object references inside new classes. For example, suppose you’d like an object that holds several String objects, a couple of primitives, and an object of another class. For the non- primitive objects, you put references inside your new class, but you define the primitives directly:

<!--p188-->
```java
//: reusing/SprinklerSystem.java
// Composition for code reuse.
class WaterSource {
private String s;
WaterSource() {
System.out.println("WaterSource()");
s = "Constructed";
}
public String toString() { return s; }
}
public class SprinklerSystem {
private String valve1, valve2, valve3, valve4;
private WaterSource source = new WaterSource();
private int i;
private float f;
public String toString() {
return
"valve1 = " + valve1 + " " +
"valve2 = " + valve2 + " " +
"valve3 = " + valve3 + " " +
"valve4 = " + valve4 + "\n" +
"i = " + i + " " + "f = " + f + " " +
"source = " + source;
}
public static void main(String[] args) {
SprinklerSystem sprinklers = new SprinklerSystem();
System.out.println(sprinklers);
}
} /* Output:
WaterSource()
valve1 = null valve2 = null valve3 = null valve4 = null
i = 0 f = 0.0 source = Constructed
*///:
```
One of the methods defined in both classes is special: toString( ). Every non-primitive object has a toString( ) method, and it’s called in special situations when the compiler wants a String but it has an object. So in the expression in SprinklerSystem.toString( ):
```java
"source = " + source;
```
the compiler sees you trying to add a String object ("source = ") to a WaterSource. Because you can only “add” a String to another String, it says “I’ll turn source into a String by calling toString( )!” After doing this it can combine the two Strings and pass the resulting String to System.out.println( ) (or equivalently, this book’s print() and printnb( ) static methods). Any time you want to allow this behavior with a class you create, you need only write a toString( ) method. Primitives that are fields in a class are automatically initialized to zero, as noted in the Everything Is an Object chapter. But the object references are initialized to null, and if you try to call methods for any of them, you’ll get an exception-a runtime error. Conveniently, you can still print a null reference without throwing an exception. It makes sense that the compiler doesn’t just create a default object for every reference, because that would incur unnecessary overhead in many cases. If you want the references initialized, you can do it: 1.At the point the objects are defined. This means that they’ll always be initialized before the constructor is called. 2.In the constructor for that class. 3. Right before you actually need to use the object. This is often called lazy initialization. It can reduce overhead in situations where object creation is expensive and the object doesn’t need to be created every time. 4.Using instance initialization. All four approaches are shown here:

<!--p189-->
```java
//: reusing/Bath.java
// Constructor initialization with composition.
import static net.mindview.util.Print.*;
class Soap {
private String s;
Soap() {
print("Soap()");
s = "Constructed";
}
public String toString() { return s; }
}
public class Bath {
private String // Initializing at point of definition:
s1 = "Happy",
s2 = "Happy",
s3, s4;
private Soap castille;
private int i;
private float toy;
public Bath() {
print("Inside Bath()");
s3 = "Joy";
toy = 3.14f;
castille = new Soap();
}
// Instance initialization:
{ i = 47; }
public String toString() {
if(s4 == null) // Delayed initialization:
s4 = "Joy";
return
"s1 = " + s1 + "\n" +
"s2 = " + s2 + "\n" +
"s3 = " + s3 + "\n" +
"s4 = " + s4 + "\n" +
"i = " + i + "\n" +
"toy = " + toy + "\n" +
"castille = " + castille;
}
public static void main(String[] args) {
Bath b = new Bath();
print(b);
}
} /* Output:
Inside Bath()
Soap()
s1 = Happy
s2 = Happy
s3 = Joy
s4 = Joy
i = 47
toy = 3.14
castille = Constructed
*///:~
```

<!--p190-->
Note that in the Bath constructor, a statement is executed before any of the initializations take place. When you don’t initialize at the point of definition, there’s still no guarantee that you’ll perform any initialization before you send a message to an object reference—except for the inevitable run-time exception. When toString( ) is called it fills in s4 so that all the fields are properly initialized by the time they are used. Exercise 1:(2) Create a simple class. Inside a second class, define a reference to an object of the first class. Use lazy initialization to instantiate this object. Reusing Classes Inheritance syntax Inheritance is an integral part of Java (and all OOP languages). It turns out that you’re always doing inheritance when you create a class, because unless you explicitly inherit from some other class, you implicitly inherit from Java’s standard root class Object. The syntax for composition is obvious, but to perform inheritance there’s a distinctly different form. When you inherit, you say “This new class is like that old class.” You state this in code before the opening brace of the class body, using the keyword extends followed by the name of the base class. When you do this, you automatically get all the fields and methods in the base class. Here’s an example:
```java
//: reusing/Detergent.java
// Inheritance syntax & properties.
import static net.mindview.util.Print.*;
class Cleanser {
private String s = "Cleanser";
public void append(String a) { s += a; }
public void dilute() { append(" dilute()"); }
public void apply() { append(" apply()"); }
public void scrub() { append(" scrub()"); }
public String toString() { return s; }
public static void main(String[] args) {
Cleanser x = new Cleanser();
x.dilute(); x.apply(); x.scrub();
print(x);
}
}
public class Detergent extends Cleanser {
// Change a method:
public void scrub() {
append(" Detergent.scrub()");
super.scrub(); // Call base-class version
}
// Add methods to the interface:
public void foam() { append(" foam()"); }
// Test the new class:
public static void main(String[] args) {
Detergent x = new Detergent();
x.dilute();
x.apply();
x.scrub();
x.foam();
print(x);
print("Testing base class:");
Cleanser.main(args);
}
} /* Output:
Cleanser dilute() apply() Detergent.scrub() scrub() foam()
Testing base class:
Cleanser dilute() apply() scrub()
*///:~
```

<!--p191-->

<!--p192-->
This demonstrates a number of features. First, in the Cleanserappend( ) method, Strings are concatenated to s using the += operator, which is one of the operators (along with ‘+’) that the Java designers “overloaded” to work with Strings. Second, both Cleanser and Detergent contain a main( ) method. You can create a main( ) for each one of your classes; this technique of putting a main() in each class allows easy testing for each class. And you don’t need to remove the main() when you’re finished; you can leave it in for later testing. Even if you have a lot of classes in a program, only the main( ) for the class invoked on the command line will be called. So in this case, when you say java Detergent, Detergent.main( ) will be called. But you can also say java Cleanser to invoke Cleanser.main( ), even though Cleanser is not a public class. Even if a class has package access, a public main() is accessible. Here, you can see that Detergent.main( ) calls Cleanser.main( ) explicitly, passing it the same arguments from the command line (however, you could pass it any String array). It’s important that all of the methods in Cleanser are public. Remember that if you leave off any access specifier, the member defaults to package access, which allows access only to package members. Thus, within this package, anyone could use those methods if there were no access specifier. Detergent would have no trouble, for example. However, if a class from some other package were to inherit from Cleanser, it could access only public members. So to allow for inheritance, as a general rule make all fields private and all methods public. (protected members also allow access by derived classes; you’ll learn about this later.) Of course, in particular cases you must make adjustments, but this is a useful guideline. Cleanser has a set of methods in its interface: append( ), dilute( ), apply( ), scrub( ), and toString( ). Because Detergent is derived fromCleanser (via the extends keyword), it automatically gets all these methods in its interface, even though you don’t see them all explicitly defined in Detergent. You can think of inheritance, then, as reusing the class. As seen in scrub( ), it’s possible to take a method that’s been defined in the base class and modify it. In this case, you might want to call the method from the base class inside the new version. But inside scrub( ), you cannot simply call scrub( ), since that would produce a recursive call, which isn’t what you want. To solve this problem, Java has the keyword super that refers to the “superclass” that the current class inherits. Thus the expression super.scrub( ) calls the base-class version of the method scrub( ). When inheriting you’re not restricted to using the methods of the base class. You can also add new methods to the derived class exactly the way you put any method in a class: Just define it. The method foam( ) is an example of this. In Detergent.main( ) you can see that for a Detergent object, you can call all the methods that are available in Cleanser as well as in Detergent (i.e., foam( )). Exercise 2: (2) Inherit a new class from class Detergent. Override scrub( ) and add a new method called sterilize( ). Initializing the base class Since there are now two classes involved—the base class and the derived class—instead of just one, it can be a bit confusing to try to imagine the resulting object produced by a derived class. From the outside, it looks like the new class has the same interface as the base class and maybe some additional methods and fields. But inheritance doesn’t just copy the interface of the base class. When you create an object of the derived class, it contains within it a subobject of the base class. This subobject is the same as if you had created an object of the base class by itself. It’s just that from the outside, the subobject of the base class is wrapped within the derived-class object. Reusing Classes Of course, it’s essential that the base-class subobject be initialized correctly, and there’s only one way to guarantee this: Perform the initialization in the constructor by calling the base- class constructor, which has all the appropriate knowledge and privileges to perform the base-class initialization. Java automatically inserts calls to the base-class constructor in the derived-class constructor. The following example shows this working with three levels of inheritance:
```java
//: reusing/Cartoon.java
// Constructor calls during inheritance.
import static net.mindview.util.Print.*;
class Art {
Art() { print("Art constructor"); }
}
class Drawing extends Art {
Drawing() { print("Drawing constructor"); }
}
public class Cartoon extends Drawing {
public Cartoon() { print("Cartoon constructor"); }
public static void main(String[] args) {
Cartoon x = new Cartoon();
}
} /* Output:
Art constructor
Drawing constructor
Cartoon constructor
*///:~
```
You can see that the construction happens from the base “outward,” so the base class is initialized before the derived-class constructors can access it. Even if you don’t create a constructor for Cartoon( ), the compiler will synthesize a default constructor for you that calls the base class constructor. Exercise 3: (2) Prove the previous sentence. Exercise 4: (2) Prove that the base-class constructors are (a) always called and (b) called before derived-class constructors. Exercise 5: (1) Create two classes, A and B, with default constructors (empty argument lists) that announce themselves. Inherit a new class called C from A, and create a member of class B inside C. Do not create a constructor for C. Create an object of class C and observe the results. Constructors with arguments The preceding example has default constructors; that is, they don’t have any arguments. It’s easy for the compiler to call these because there’s no question about what arguments to pass. If your class doesn’t have default arguments, or if you want to call a base-class constructor that has an argument, you must explicitly write the calls to the base-class constructor using the super keyword and the appropriate argument list:

<!--p193-->
```java
//: reusing/Chess.java
// Inheritance, constructors and arguments.
import static net.mindview.util.Print.*;
class Game {
Game(int i) {
print("Game constructor");
}
}
class BoardGame extends Game {
BoardGame(int i) {
super(i);
print("BoardGame constructor");
}
}
public class Chess extends BoardGame {
Chess() {
super(11);
print("Chess constructor");
}
public static void main(String[] args) {
Chess x = new Chess();
}
} /* Output:
Game constructor
BoardGame constructor
Chess constructor
*///:~
```
If you don’t call the base-class constructor in BoardGame( ), the compiler will complain that it can’t find a constructor of the form Game( ). In addition, the call to the base-class constructor must be the first thing you do in the derived-class constructor. (The compiler will remind you if you get it wrong.) Exercise 6: (1) Using Chess.java, prove the statements in the previous paragraph. Exercise 7: (1) Modify Exercise 5 so that A and B have constructors with arguments instead of default constructors. Write a constructor for C and perform all initialization within C’s constructor. Exercise 8: (1) Create a base class with only a non-default constructor, and a derived class with both a default (no-arg) and non-default constructor. In the derived-class constructors, call the base-class constructor. Exercise 9: (2) Create a class called Root that contains an instance of each of the classes (that you also create) named Component1, Component2, and Component3. Derive a class Stem from Root that also contains an instance of each “component.” All classes should have default constructors that print a message about that class. Exercise 10: (1) Modify the previous exercise so that each class only has non-default constructors. Delegation A third relationship, which is not directly supported by Java, is called delegation. This is midway between inheritance and composition, because you place a member object in the class you’re building (like composition), but at the same time you expose all the methods from the member object in your new class (like inheritance). For example, a spaceship needs a control module:
```java
//: reusing/SpaceShipControls.java
```

<!--p194-->
Reusing Classes
```java
public class SpaceShipControls {
void up(int velocity) {}
void down(int velocity) {}
void left(int velocity) {}
void right(int velocity) {}
void forward(int velocity) {}
void back(int velocity) {}
void turboBoost() {}
} ///:~
```
One way to build a spaceship is to use inheritance:
```java
//: reusing/SpaceShip.java
public class SpaceShip extends SpaceShipControls {
private String name;
public SpaceShip(String name) { this.name = name; }
public String toString() { return name; }
public static void main(String[] args) {
SpaceShip protector = new SpaceShip("NSEA Protector");
protector.forward(100);
}
} ///:~
```
However, a SpaceShip isn’t really “a type of” SpaceShipControls, even if, for example, you “tell” a SpaceShip to go forward( ). It’s more accurate to say that a SpaceShip contains SpaceShipControls, and at the same time all the methods in SpaceShipControls are exposed in a SpaceShip. Delegation solves the dilemma:

<!--p195-->
```java
//: reusing/SpaceShipDelegation.java
public class SpaceShipDelegation {
private String name;
private SpaceShipControls controls =
new SpaceShipControls();
public SpaceShipDelegation(String name) {
this.name = name;
}
// Delegated methods:
public void back(int velocity) {
controls.back(velocity);
}
public void down(int velocity) {
controls.down(velocity);
}
public void forward(int velocity) {
controls.forward(velocity);
}
public void left(int velocity) {
controls.left(velocity);
}
public void right(int velocity) {
controls.right(velocity);
}
public void turboBoost() {
controls.turboBoost();
}
public void up(int velocity) {
controls.up(velocity);
}
public static void main(String[] args) {
SpaceShipDelegation protector =
new SpaceShipDelegation("NSEA Protector");
protector.forward(100);
}
} ///:~
```
You can see how the methods are forwarded to the underlying controls object, and the interface is thus the same as it is with inheritance. However, you have more control with delegation because you can choose to provide only a subset of the methods in the member object. Although the Java language doesn’t support delegation, development tools often do. The above example, for instance, was automatically generated using the JetBrains Idea IDE. Exercise 11: (3) Modify Detergent.java so that it uses delegation. Combining composition and inheritance It is very common to use composition and inheritance together. The following example shows the creation of a more complex class, using both inheritance and composition, along with the necessary constructor initialization:
```java
//: reusing/PlaceSetting.java
// Combining composition & inheritance.
import static net.mindview.util.Print.*;
class Plate {
Plate(int i) {
print("Plate constructor");
}
}
class DinnerPlate extends Plate {
DinnerPlate(int i) {
super(i);
print("DinnerPlate constructor");
}
}
class Utensil {
Utensil(int i) {
print("Utensil constructor");
}
}
class Spoon extends Utensil {
Spoon(int i) {
super(i);
print("Spoon constructor");
}
}
class Fork extends Utensil {
Fork(int i) {
super(i);
print("Fork constructor");
}
```

<!--p196-->
Reusing Classes
```java
}
class Knife extends Utensil {
Knife(int i) {
super(i);
print("Knife constructor");
}
}
// A cultural way of doing something:
class Custom {
Custom(int i) {
print("Custom constructor");
}
}
public class PlaceSetting extends Custom {
private Spoon sp;
private Fork frk;
private Knife kn;
private DinnerPlate pl;
public PlaceSetting(int i) {
super(i + 1);
sp = new Spoon(i + 2);
frk = new Fork(i + 3);
kn = new Knife(i + 4);
pl = new DinnerPlate(i + 5);
print("PlaceSetting constructor");
}
public static void main(String[] args) {
PlaceSetting x = new PlaceSetting(9);
}
} /* Output:
Custom constructor
Utensil constructor
Spoon constructor
Utensil constructor
Fork constructor
Utensil constructor
Knife constructor
Plate constructor
DinnerPlate constructor
PlaceSetting constructor
*///:~
```

<!--p197-->
Although the compiler forces you to initialize the base classes, and requires that you do it right at the beginning of the constructor, it doesn’t watch over you to make sure that you initialize the member objects, so you must remember to pay attention to that. It’s rather amazing how cleanly the classes are separated. You don’t even need the source code for the methods in order to reuse the code. At most, you just import a package. (This is true for both inheritance and composition.) Guaranteeing proper cleanup Java doesn’t have the C++ concept of a destructor, a method that is automatically called when an object is destroyed. The reason is probably that in Java, the practice is simply to forget about objects rather than to destroy them, allowing the garbage collector to reclaim the memory as necessary. Often this is fine, but there are times when your class might perform some activities during its lifetime that require cleanup. As mentioned in the Initialization & Cleanup chapter, you can’t know when the garbage collector will be called, or if it will be called. So if you want something cleaned up for a class, you must explicitly write a special method to do it, and make sure that the client programmer knows that they must call this method. On top of this—as described in the Error Handling with Exceptions chapter—you must guard against an exception by putting such cleanup in a finally clause. Consider an example of a computer-aided design system that draws pictures on the screen:
```java
//: reusing/CADSystem.java
// Ensuring proper cleanup.
package reusing;
import static net.mindview.util.Print.*;
class Shape {
Shape(int i) { print("Shape constructor"); }
void dispose() { print("Shape dispose"); }
}
class Circle extends Shape {
Circle(int i) {
super(i);
print("Drawing Circle");
}
void dispose() {
print("Erasing Circle");
super.dispose();
}
}
class Triangle extends Shape {
Triangle(int i) {
super(i);
print("Drawing Triangle");
}
void dispose() {
print("Erasing Triangle");
super.dispose();
}
}
class Line extends Shape {
private int start, end;
Line(int start, int end) {
super(start);
this.start = start;
this.end = end;
print("Drawing Line: " + start + ", " + end);
}
void dispose() {
print("Erasing Line: " + start + ", " + end);
super.dispose();
}
}
public class CADSystem extends Shape {
private Circle c;
private Triangle t;
private Line[] lines = new Line[3];
public CADSystem(int i) {
super(i + 1);
```

<!--p198-->
Reusing Classes
```java
for(int j = 0; j < lines.length; j++)
lines[j] = new Line(j, j*j);
c = new Circle(1);
t = new Triangle(1);
print("Combined constructor");
}
public void dispose() {
print("CADSystem.dispose()");
// The order of cleanup is the reverse
// of the order of initialization:
t.dispose();
c.dispose();
for(int i = lines.length - 1; i >= 0; i--)
lines[i].dispose();
super.dispose();
}
public static void main(String[] args) {
CADSystem x = new CADSystem(47);
try {
// Code and exception handling...
} finally {
x.dispose();
}
}
} /* Output:
Shape constructor
Shape constructor
Drawing Line: 0, 0
Shape constructor
Drawing Line: 1, 1
Shape constructor
Drawing Line: 2, 4
Shape constructor
Drawing Circle
Shape constructor
Drawing Triangle
Combined constructor
CADSystem.dispose()
Erasing Triangle
Shape dispose
Erasing Circle
Shape dispose
Erasing Line: 2, 4
Shape dispose
Erasing Line: 1, 1
Shape dispose
Erasing Line: 0, 0
Shape dispose
Shape dispose
*///:~
```

<!--p199-->
Everything in this system is some kind of Shape (which is itself a kind of Object, since it’s implicitly inherited from the root class). Each class overrides Shape’s dispose( ) method in addition to calling the base-class version of that method using super. The specific Shape classes—Circle, Triangle, and Line—all have constructors that “draw,” although any method called during the lifetime of the object could be responsible for doing something that needs cleanup. Each class has its own dispose( ) method to restore non-memory things back to the way they were before the object existed. In main( ), you can see two keywords that are new, and won’t be explained until the Error Handling with Exceptions chapter: try and finally. The try keyword indicates that the block that follows (delimited by curly braces) is a guarded region, which means that it is given special treatment. One of these special treatments is that the code in the finally clause following this guarded region is always executed, no matter how the try block exits. (With exception handling, it’s possible to leave a try block in a number of non-ordinary ways.) Here, the finally clause is saying “always call dispose( ) for x, no matter what happens.” Note that in your cleanup method, you must also pay attention to the calling order for the base-class and member-object cleanup methods in case one subobject depends on another. In general, you should follow the same form that is imposed by a C++ compiler on its destructors: First perform all of the cleanup work specific to your class, in the reverse order of creation. (In general, this requires that base-class elements still be viable.) Then call the base-class cleanup method, as demonstrated here. There can be many cases in which the cleanup issue is not a problem; you just let the garbage collector do the work. But when you must do it explicitly, diligence and attention are required, because there’s not much you can rely on when it comes to garbage collection. The garbage collector might never be called. If it is, it can reclaim objects in any order it wants. You can’t rely on garbage collection for anything but memory reclamation. If you want cleanup to take place, make your own cleanup methods and don’t use on finalize( ). Exercise 12: (3) Add a proper hierarchy of dispose( ) methods to all the classes in Exercise 9. Name hiding If a Java base class has a method name that’s overloaded several times, redefining that method name in the derived class will not hide any of the base-class versions (unlike C++). Thus overloading works regardless of whether the method was defined at this level or in a base class:
```java
//: reusing/Hide.java
// Overloading a base-class method name in a derived
// class does not hide the base-class versions.
import static net.mindview.util.Print.*;
class Homer {
char doh(char c) {
print("doh(char)");
return ‘d’;
}
float doh(float f) {
print("doh(float)");
return 1.0f;
}
}
class Milhouse {}
class Bart extends Homer {
void doh(Milhouse m) {
print("doh(Milhouse)");
}
}
public class Hide {
public static void main(String[] args) {
Bart b = new Bart();
b.doh(1);
b.doh(‘x’);
b.doh(1.0f);
```

<!--p200-->
Reusing Classes
```java
b.doh(new Milhouse());
}
} /* Output:
doh(float)
doh(char)
doh(float)
doh(Milhouse)
*///:~
```
You can see that all the overloaded methods of Homer are available in Bart, even though Bart introduces a new overloaded method (in C++ doing this would hide the base-class methods). As you’ll see in the next chapter, it’s far more common to override methods of the same name, using exactly the same signature and return type as in the base class. It can be confusing otherwise (which is why C++ disallows it—to prevent you from making what is probably a mistake). Java SE5 has added the @Override annotation, which is not a keyword but can be used as if it were. When you mean to override a method, you can choose to add this annotation and the compiler will produce an error message if you accidentally overload instead of overriding.
```java
//: reusing/Lisa.java
// {CompileTimeError} (Won’t compile)
class Lisa extends Homer {
@Override void doh(Milhouse m) {
System.out.println("doh(Milhouse)");
}
} ///:~
```
The {CompileTimeError} tag excludes the file from this book’s Ant build, but if you compile it by hand you’ll see the error message:
```java
method does not override a method from its superclass
```

<!--p201-->
The @Override annotation will thus prevent you from accidentally overloading when you don’t mean to. Exercise 13: (2) Create a class with a method that is overloaded three times. Inherit a new class, add a new overloading of the method, and show that all four methods are available in the derived class. Choosing composition vs. inheritance Both composition and inheritance allow you to place subobjects inside your new class (composition explicitly does this—with inheritance it’s implicit). You might wonder about the difference between the two, and when to choose one over the other. Composition is generally used when you want the features of an existing class inside your new class, but not its interface. That is, you embed an object so that you can use it to implement features in your new class, but the user of your new class sees the interface you’ve defined for the new class rather than the interface from the embedded object. For this effect, you embed private objects of existing classes inside your new class. Sometimes it makes sense to allow the class user to directly access the composition of your new class; that is, to make the member objects public. The member objects use implementation hiding themselves, so this is a safe thing to do. When the user knows you’re assembling a bunch of parts, it makes the interface easier to understand. A car object is a good example:
```java
//: reusing/Car.java
// Composition with public objects.
class Engine {
public void start() {}
public void rev() {}
public void stop() {}
}
class Wheel {
public void inflate(int psi) {}
}
class Window {
public void rollup() {}
public void rolldown() {}
}
class Door {
public Window window = new Window();
public void open() {}
public void close() {}
}
public class Car {
public Engine engine = new Engine();
public Wheel[] wheel = new Wheel[4];
public Door
left = new Door(),
right = new Door(); // 2-door
public Car() {
for(int i = 0; i < 4; i++)
wheel[i] = new Wheel();
}
public static void main(String[] args) {
Car car = new Car();
car.left.window.rollup();
car.wheel[0].inflate(72);
}
} ///:~
```

<!--p202-->
Because in this case the composition of a car is part of the analysis of the problem (and not simply part of the underlying design), making the members public assists the client programmer’s understanding of how to use the class and requires less code complexity for the creator of the class. However, keep in mind that this is a special case, and that in general you should make fields private. When you inherit, you take an existing class and make a special version of it. In general, this means that you’re taking a general-purpose class and specializing it for a particular need. With a little thought, you’ll see that it would make no sense to compose a car using a vehicle object—a car doesn’t contain a vehicle, it is a vehicle. The is-a relationship is expressed with inheritance, and the has-a relationship is expressed with composition. Exercise 14: (1) In Car.java add a service( ) method to Engine and call this method in main( ). Reusing Classes
## protected
Now that you’ve been introduced to inheritance, the keyword protected finally has meaning. In an ideal world, the private keyword would be enough. In real projects, there are times when you want to make something hidden from the world at large and yet allow access for members of derived classes. The protected keyword is a nod to pragmatism. It says “This is private as far as the class user is concerned, but available to anyone who inherits from this class or anyone else in the same package.” (In Java, protected also provides package access.) Although it’s possible to create protected fields, the best approach is to leave the fields private; you should always preserve your right to change the underlying implementation. You can then allow controlled access to inheritors of your class through protected methods:
```java
//: reusing/Orc.java
// The protected keyword.
import static net.mindview.util.Print.*;
class Villain {
private String name;
protected void set(String nm) { name = nm; }
public Villain(String name) { this.name = name; }
public String toString() {
return "I’m a Villain and my name is " + name;
}
}
public class Orc extends Villain {
private int orcNumber;
public Orc(String name, int orcNumber) {
super(name);
this.orcNumber = orcNumber;
}
public void change(String name, int orcNumber) {
set(name); // Available because it’s protected
this.orcNumber = orcNumber;
}
public String toString() {
return "Orc " + orcNumber + ": " + super.toString();
}
public static void main(String[] args) {
Orc orc = new Orc("Limburger", 12);
print(orc);
orc.change("Bob", 19);
print(orc);
}
} /* Output:
Orc 12: I’m a Villain and my name is Limburger
Orc 19: I’m a Villain and my name is Bob
*///:~
```

<!--p203-->
You can see that change( ) has access to set( ) because it’s protected. Also note the way that Orc’s toString( ) method is defined in terms of the base-class version of toString( ). Exercise 15: (2) Create a class inside a package. Your class should contain a protected method. Outside of the package, try to call the protected method and explain the results. Now inherit from your class and call the protected method from inside a method of your derived class. Upcasting The most important aspect of inheritance is not that it provides methods for the new class. It’s the relationship expressed between the new class and the base class. This relationship can be summarized by saying, “The new class is a type of the existing class.” This description is not just a fanciful way of explaining inheritance—it’s supported directly by the language. As an example, consider a base class called Instrument that represents musical instruments, and a derived class called Wind. Because inheritance means that all of the methods in the base class are also available in the derived class, any message you can send to the base class can also be sent to the derived class. If the Instrument class has a play( ) method, so will Wind instruments. This means we can accurately say that a Wind object is also a type of Instrument. The following example shows how the compiler supports this notion:
```java
//: reusing/Wind.java
// Inheritance & upcasting.
class Instrument {
public void play() {}
static void tune(Instrument i) {
// ...
i.play();
}
}
// Wind objects are instruments
// because they have the same interface:
public class Wind extends Instrument {
public static void main(String[] args) {
Wind flute = new Wind();
Instrument.tune(flute); // Upcasting
}
} ///:~
```

<!--p204-->
What’s interesting in this example is the tune( ) method, which accepts an Instrument reference. However, in Wind.main( ) the tune( ) method is called by giving it a Wind reference. Given that Java is particular about type checking, it seems strange that a method that accepts one type will readily accept another type, until you realize that a Wind object is also an Instrument object, and there’s no method that tune( ) could call for an Instrument that isn’t also in Wind. Inside tune( ), the code works for Instrument and anything derived from Instrument, and the act of converting a Wind reference into an Instrument reference is called upcasting. Why “upcasting”? The term is based on the way that class inheritance diagrams have traditionally been drawn: with the root at the top of the page, growing downward. (Of course, you can draw your diagrams any way you find helpful.) The inheritance diagram for Wind.java is then: Reusing Classes Casting from a derived type to a base type moves up on the inheritance diagram, so it’s commonly referred to as upcasting. Upcasting is always safe because you’re going from a more specific type to a more general type. That is, the derived class is a superset of the base class. It might contain more methods than the base class, but it must contain at least the methods in the base class. The only thing that can occur to the class interface during the upcast is that it can lose methods, not gain them. This is why the compiler allows upcasting without any explicit casts or other special notation. You can also perform the reverse of upcasting, called downcasting, but this involves a dilemma that will be examined further in the next chapter, and in the Type Information chapter. Composition vs. inheritance revisited In object-oriented programming, the most likely way that you’ll create and use code is by simply packaging data and methods together into a class, and using objects of that class. You’ll also use existing classes to build new classes with composition. Less frequently, you’ll use inheritance. So although inheritance gets a lot of emphasis while learning OOP, it doesn’t mean that you should use it everywhere you possibly can. On the contrary, you should use it sparingly, only when it’s clear that inheritance is useful. One of the clearest ways to determine whether you should use composition or inheritance is to ask whether you’ll ever need to upcast from your new class to the base class. If you must upcast, then inheritance is necessary, but if you don’t need to upcast, then you should look closely at whether you need inheritance. The Polymorphism chapter provides one of the most compelling reasons for upcasting, but if you remember to ask “Do I need to upcast?” you’ll have a good tool for deciding between composition and inheritance. Exercise 16: (2) Create a class called Amphibian. From this, inherit a class called Frog. Put appropriate methods in the base class. In main( ), create a Frog and upcast it to Amphibian and demonstrate that all the methods still work. Exercise 17: (1) Modify Exercise 16 so that Frog overrides the method definitions from the base class (provides new definitions using the same method signatures). Note what happens in main( ).
## The final keyword

<!--p205-->
Java’s final keyword has slightly different meanings depending on the context, but in general it says “This cannot be changed.” You might want to prevent changes for two reasons: design or efficiency. Because these two reasons are quite different, it’s possible to misuse the final keyword. The following sections discuss the three places where final can be used: for data, methods, and classes.
## final data
Many programming languages have a way to tell the compiler that a piece of data is “constant.” A constant is useful for two reasons: 1.It can be a compile-time constant that won’t ever change. 2.It can be a value initialized at run time that you don’t want changed. In the case of a compile-time constant, the compiler is allowed to “fold” the constant value into any calculations in which it’s used; that is, the calculation can be performed at compile time, eliminating some run-time overhead. In Java, these sorts of constants must be primitives and are expressed with the final keyword. A value must be given at the time of definition of such a constant. A field that is both static and final has only one piece of storage that cannot be changed. When final is used with object references rather than primitives, the meaning can be confusing. With a primitive, final makes the value a constant, but with an object reference, final makes the reference a constant. Once the reference is initialized to an object, it can never be changed to point to another object. However, the object itself can be modified; Java does not provide a way to make any arbitrary object a constant. (You can, however, write your class so that objects have the effect of being constant.) This restriction includes arrays, which are also objects. Here’s an example that demonstrates final fields. Note that by convention, fields that are both static and final (that is, compile-time constants) are capitalized and use underscores to separate words.
```java
//: reusing/FinalData.java
// The effect of final on fields.
import java.util.*;
import static net.mindview.util.Print.*;
class Value {
int i; // Package access
public Value(int i) { this.i = i; }
}
public class FinalData {
private static Random rand = new Random(47);
private String id;
public FinalData(String id) { this.id = id; }
// Can be compile-time constants:
private final int valueOne = 9;
private static final int VALUE_TWO = 99;
// Typical public constant:
public static final int VALUE_THREE = 39;
// Cannot be compile-time constants:
private final int i4 = rand.nextInt(20);
static final int INT_5 = rand.nextInt(20);
private Value v1 = new Value(11);
private final Value v2 = new Value(22);
private static final Value VAL_3 = new Value(33);
// Arrays:
private final int[] a = { 1, 2, 3, 4, 5, 6 };
public String toString() {
return id + ": " + "i4 = " + i4 + ", INT_5 = " + INT_5;
}
```

<!--p206-->
Reusing Classes
```java
public static void main(String[] args) {
FinalData fd1 = new FinalData("fd1");
//! fd1.valueOne++; // Error: can’t change value
fd1.v2.i++; // Object isn’t constant!
fd1.v1 = new Value(9); // OK -- not final
for(int i = 0; i < fd1.a.length; i++)
fd1.a[i]++; // Object isn’t constant!
//! fd1.v2 = new Value(0); // Error: Can’t
//! fd1.VAL_3 = new Value(1); // change reference
//! fd1.a = new int[3];
print(fd1);
print("Creating new FinalData");
FinalData fd2 = new FinalData("fd2");
print(fd1);
print(fd2);
}
} /* Output:
fd1: i4 = 15, INT_5 = 18
Creating new FinalData
fd1: i4 = 15, INT_5 = 18
fd2: i4 = 13, INT_5 = 18
*///:~
```
Since valueOne and VALUE_TWO are final primitives with compile-time values, they can both be used as compile-time constants and are not different in any important way. VALUE_THREE is the more typical way you’ll see such constants defined: public so they’re usable outside the package, static to emphasize that there’s only one, and final to say that it’s a constant. Note that final static primitives with constant initial values (that is, compile-time constants) are named with all capitals by convention, with words separated by underscores. (This is just like C constants, which is where the convention originated.) Just because something is final doesn’t mean that its value is known at compile time. This is demonstrated by initializing i4 and INT_5 at run time using randomly generated numbers. This portion of the example also shows the difference between making a final value static or non-static. This difference shows up only when the values are initialized at run time, since the compile-time values are treated the same by the compiler. (And presumably optimized out of existence.) The difference is shown when you run the program. Note that the values of i4 for fd1 and fd2 are unique, but the value for INT_5 is not changed by creating the second FinalData object. That’s because it’s static and is initialized once upon loading and not each time a new object is created. The variables v1 through VAL_3 demonstrate the meaning of a final reference. As you can see in main( ), just because v2 is final doesn’t mean that you can’t change its value. Because it’s a reference, final means that you cannot rebind v2 to a new object. You can also see that the same meaning holds true for an array, which is just another kind of reference. (There is no way that I know of to make the array references themselves final.) Making references final seems less useful than making primitives final. Exercise 18: (2) Create a class with a static final field and a final field and demonstrate the difference between the two.
## Blank finals

<!--p207-->
Java allows the creation of blank finals, which are fields that are declared as final but are not given an initialization value. In all cases, the blank final must be initialized before it is used, and the compiler ensures this. However, blank finals provide much more flexibility in the use of the final keyword since, for example, a final field inside a class can now be different for each object, and yet it retains its immutable quality. Here’s an example:
```java
//: reusing/BlankFinal.java
// "Blank" final fields.
class Poppet {
private int i;
Poppet(int ii) { i = ii; }
}
public class BlankFinal {
private final int i = 0; // Initialized final
private final int j; // Blank final
private final Poppet p; // Blank final reference
// Blank finals MUST be initialized in the constructor:
public BlankFinal() {
j = 1; // Initialize blank final
p = new Poppet(1); // Initialize blank final reference
}
public BlankFinal(int x) {
j = x; // Initialize blank final
p = new Poppet(x); // Initialize blank final reference
}
public static void main(String[] args) {
new BlankFinal();
new BlankFinal(47);
}
} ///:~
```
You’re forced to perform assignments to finals either with an expression at the point of definition of the field or in every constructor. That way it’s guaranteed that the final field is always initialized before use. Exercise 19: (2) Create a class with a blank final reference to an object. Perform the initialization of the blank final inside all constructors. Demonstrate the guarantee that the final must be initialized before use, and that it cannot be changed once initialized.
## final arguments
Java allows you to make arguments final by declaring them as such in the argument list. This means that inside the method you cannot change what the argument reference points to:
```java
//: reusing/FinalArguments.java
// Using "final" with method arguments.
class Gizmo {
public void spin() {}
}
public class FinalArguments {
void with(final Gizmo g) {
//! g = new Gizmo(); // Illegal -- g is final
}
void without(Gizmo g) {
g = new Gizmo(); // OK -- g not final
g.spin();
}
// void f(final int i) { i++; } // Can’t change
// You can only read from a final primitive:
int g(final int i) { return i + 1; }
public static void main(String[] args) {
FinalArguments bf = new FinalArguments();
```

<!--p208-->
Reusing Classes
```java
bf.without(null);
bf.with(null);
}
} ///:~
```
The methods f( ) and g( ) show what happens when primitive arguments are final: You can read the argument, but you can’t change it. This feature is primarily used to pass data to anonymous inner classes, which you’ll learn about in the Inner Classes chapter.
## final methods
There are two reasons for final methods. The first is to put a “lock” on the method to prevent any inheriting class from changing its meaning. This is done for design reasons when you want to make sure that a method’s behavior is retained during inheritance and cannot be overridden. The second reason for final methods is efficiency. In earlier implementations of Java, if you made a method final, you allowed the compiler to turn any calls to that method into inline calls. When the compiler saw a final method call, it could (at its discretion) skip the normal approach of inserting code to perform the method call mechanism (push arguments on the stack, hop over to the method code and execute it, hop back and clean off the stack arguments, and deal with the return value) and instead replace the method call with a copy of the actual code in the method body. This eliminated the overhead of the method call. Of course, if a method is big, then your code begins to bloat, and you probably wouldn’t see any performance gains from inlining, since any improvements will be dwarfed by the amount of time spent inside the method. In more recent version of Java, the virtual machine (in particular, the hotspot technologies) can detect these situations and optimize away the extra indirection, so its no longer necessary-in fact, it is now generally discouraged-to use final to try to help the optimizer. With Java SE5/6, you should let the compiler and JVM handle efficiency issues and make a method final only if you want to explicitly prevent overriding.1
## final and private
Any private methods in a class are implicitly final. Because you can’t access a private method, you can’t override it. You can add the final specifier to a private method, but it doesn’t give that method any extra meaning. This issue can cause confusion, because if you try to override a private method (which is implicitly final), it seems to work, and the compiler doesn’t give an error message:
```java
//: reusing/FinalOverridingIllusion.java
// It only looks like you can override
// a private or private final method.
import static net.mindview.util.Print.*;
class WithFinals {
// Identical to "private" alone:
private final void f() { print("WithFinals.f()"); }
// Also automatically "final":
private void g() { print("WithFinals.g()"); }
}
```

<!--p209-->
1Don’t fall prey to the urge to prematurely optimize. If you get your system working and it’s too slow, it’s doubtful that you can fix it with the final keyword. http://MindView.net/Books/BetterJava has information about profiling, which can be helpful in speeding up your program.
```java
class OverridingPrivate extends WithFinals {
private final void f() {
print("OverridingPrivate.f()");
}
private void g() {
print("OverridingPrivate.g()");
}
}
class OverridingPrivate2 extends OverridingPrivate {
public final void f() {
print("OverridingPrivate2.f()");
}
public void g() {
print("OverridingPrivate2.g()");
}
}
public class FinalOverridingIllusion {
public static void main(String[] args) {
OverridingPrivate2 op2 = new OverridingPrivate2();
op2.f();
op2.g();
// You can upcast:
OverridingPrivate op = op2;
// But you can’t call the methods:
//! op.f();
//! op.g();
// Same here:
WithFinals wf = op2;
//! wf.f();
//! wf.g();
}
} /* Output:
OverridingPrivate2.f()
OverridingPrivate2.g()
*///:~
```
“Overriding” can only occur if something is part of the base-class interface. That is, you must be able to upcast an object to its base type and call the same method (the point of this will become clear in the next chapter). If a method is private, it isn’t part of the base-class interface. It is just some code that’s hidden away inside the class, and it just happens to have that name, but if you create a public, protected, or package-access method with the same name in the derived class, there’s no connection to the method that might happen to have that name in the base class. You haven’t overridden the method; you’ve just created a new method. Since a private method is unreachable and effectively invisible, it doesn’t factor into anything except for the code organization of the class for which it was defined. Exercise 20: (1) Show that @Override annotation solves the problem in this section. Exercise 21: (1) Create a class with a final method. Inherit from that class and attempt to overwrite that method.
## final classes

<!--p210-->
When you say that an entire class is final (by preceding its definition with the final keyword), you state that you don’t want to inherit from this class or allow anyone else to do so. In other words, for some reason the design of your class is such that there is never a need to make any changes, or for safety or security reasons you don’t want subclassing. Reusing Classes
```java
//: reusing/Jurassic.java
// Making an entire class final.
class SmallBrain {}
final class Dinosaur {
int i = 7;
int j = 1;
SmallBrain x = new SmallBrain();
void f() {}
}
//! class Further extends Dinosaur {}
// error: Cannot extend final class ‘Dinosaur’
public class Jurassic {
public static void main(String[] args) {
Dinosaur n = new Dinosaur();
n.f();
n.i = 40;
n.j++;
}
} ///:~
```
Note that the fields of a final class can be final or not, as you choose. The same rules apply to final for fields regardless of whether the class is defined as final. However, because it prevents inheritance, all methods in a final class are implicitly final, since there’s no way to override them. You can add the final specifier to a method in a final class, but it doesn’t add any meaning. Exercise 22: (1) Create a final class and attempt to inherit from it.
## final caution

<!--p211-->
It can seem to be sensible to make a method final while you’re designing a class. You might feel that no one could possibly want to override your methods. Sometimes this is true. But be careful with your assumptions. In general, it’s difficult to anticipate how a class can be reused, especially a general-purpose class. If you define a method as final, you might prevent the possibility of reusing your class through inheritance in some other programmer’s project simply because you couldn’t imagine it being used that way. The standard Java library is a good example of this. In particular, the Java 1.0/1.1 Vector class was commonly used and might have been even more useful if, in the name of efficiency (which was almost certainly an illusion), all the methods hadn’t been made final. It’s easily conceivable that you might want to inherit and override with such a fundamentally useful class, but the designers somehow decided this wasn’t appropriate. This is ironic for two reasons. First, Stack is inherited from Vector, which says that a Stack is a Vector, which isn’t really true from a logical standpoint. Nonetheless, it’s a case where the Java designers themselves inherited Vector. At the point they created Stack this way, they should have realized that final methods were too restrictive. Second, many of the most important methods of Vector, such as addElement( ) and elementAt( ), are synchronized. As you will see in the Concurrency chapter, this imposes a significant performance overhead that probably wipes out any gains provided by final. This lends credence to the theory that programmers are consistently bad at guessing where optimizations should occur. It’s just too bad that such a clumsy design made it into the standard library, where everyone had to cope with it. (Fortunately, the modern Java Reusing Classes container library replaces Vector with ArrayList, which behaves much more civilly. Unfortunately, there’s still new code being written that uses the old container library.) It’s also interesting to note that Hashtable, another important Java 1.0/1.1 standard library class, does not have any final methods. As mentioned elsewhere in this book, it’s quite obvious that some classes were designed by completely different people than others. (You’ll see that the method names in Hashtable are much briefer compared to those in Vector, another piece of evidence.) This is precisely the sort of thing that should not be obvious to consumers of a class library. When things are inconsistent, it just makes more work for the user—yet another paean to the value of design and code walkthroughs. (Note that the modern Java container library replaces Hashtable with HashMap.) Initialization and class loading In more traditional languages, programs are loaded all at once as part of the startup process. This is followed by initialization, and then the program begins. The process of initialization in these languages must be carefully controlled so that the order of initialization of statics doesn’t cause trouble. C++, for example, has problems if one static expects another static to be valid before the second one has been initialized. Java doesn’t have this problem because it takes a different approach to loading. This is one of the activities that become easier, because everything in Java is an object. Remember that the compiled code for each class exists in its own separate file. That file isn’t loaded until the code is needed. In general, you can say that “class code is loaded at the point of first use.” This is usually when the first object of that class is constructed, but loading also occurs when a static field or static method is accessed.2 The point of first use is also where the static initialization takes place. All the static objects and the static code block will be initialized in textual order (that is, the order that you write them down in the class definition) at the point of loading. The statics, of course, are initialized only once. Initialization with inheritance It’s helpful to look at the whole initialization process, including inheritance, to get a full picture of what happens. Consider the following example:
```java
//: reusing/Beetle.java
// The full process of initialization.
import static net.mindview.util.Print.*;
class Insect {
private int i = 9;
protected int j;
Insect() {
print("i = " + i + ", j = " + j);
j = 39;
}
private static int x1 =
printInit("static Insect.x1 initialized");
static int printInit(String s) {
```

<!--p212-->
2The constructor is also a static method even though the static keyword is not explicit. So to be precise, a class is first loaded when any one of its static members is accessed.
```java
print(s);
return 47;
}
}
public class Beetle extends Insect {
private int k = printInit("Beetle.k initialized");
public Beetle() {
print("k = " + k);
print("j = " + j);
}
private static int x2 =
printInit("static Beetle.x2 initialized");
public static void main(String[] args) {
print("Beetle constructor");
Beetle b = new Beetle();
}
} /* Output:
static Insect.x1 initialized
static Beetle.x2 initialized
Beetle constructor
i = 9, j = 0
Beetle.k initialized
k = 47
j = 39
*///:~
```

<!--p213-->
The first thing that happens when you run Java on Beetle is that you try to access Beetle.main( ) (a static method), so the loader goes out and finds the compiled code for the Beetle class (this happens to be in a file called Beetle.class). In the process of loading it, the loader notices that it has a base class (that’s what the extends keyword says), which it then loads. This will happen whether or not you’re going to make an object of that base class. (Try commenting out the object creation to prove it to yourself.) If the base class has a base class, that second base class would then be loaded, and so on. Next, the static initialization in the root base class (in this case, Insect) is performed, and then the next derived class, and so on. This is important because the derived-class static initialization might depend on the base class member being initialized properly. At this point, the necessary classes have all been loaded so the object can be created. First, all the primitives in this object are set to their default values and the object references are set to null—this happens in one fell swoop by setting the memory in the object to binary zero. Then the base-class constructor will be called. In this case the call is automatic, but you can also specify the base-class constructor call (as the first operation in the Beetle( ) constructor) by using super. The base class construction goes through the same process in the same order as the derived-class constructor. After the base-class constructor completes, the instance variables are initialized in textual order. Finally, the rest of the body of the constructor is executed. Exercise 23: (2) Prove that class loading takes place only once. Prove that loading may be caused by either the creation of the first instance of that class or by the access of a static member. Exercise 24: (2) In Beetle.java, inherit a specific type of beetle from class Beetle, following the same format as the existing classes. Trace and explain the output. Reusing Classes Summary Both inheritance and composition allow you to create a new type from existing types. Composition reuses existing types as part of the underlying implementation of the new type, and inheritance reuses the interface. With Inheritance, the derived class has the base-class interface, so it can be upcast to the base, which is critical for polymorphism, as you’ll see in the next chapter. Despite the strong emphasis on inheritance in object-oriented programming, when you start a design you should generally prefer composition (or possibly delegation) during the first cut and use inheritance only when it is clearly necessary. Composition tends to be more flexible. In addition, by using the added artifice of inheritance with your member type, you can change the exact type, and thus the behavior, of those member objects at run time. Therefore, you can change the behavior of the composed object at run time. When designing a system, your goal is to find or create a set of classes in which each class has a specific use and is neither too big (encompassing so much functionality that it’s unwieldy to reuse) nor annoyingly small (you can’t use it by itself or without adding functionality). If your designs become too complex, it’s often helpful to add more objects by breaking down existing ones into smaller parts. When you set out to design a system, it’s important to realize that program development is an incremental process, just like human learning. It relies on experimentation; you can do as much analysis as you want, but you still won’t know all the answers when you set out on a project. You’ll have much more success-and more immediate feedback-if you start out to “grow” your project as an organic, evolutionary creature, rather than constructing it all at once like a glass-box skyscraper. Inheritance and composition are two of the most fundamental tools in object-oriented programming that allow you to perform such experiments. Solutions to selected exercises can be found in the electronic document The Thinking in Java Annotated Solution Guide, available for sale from www.MindView.net.