# 8. Polymorphism (printed p193-218)


<!--p215-->
Polymorphism ”I have been asked, ‘Pray, Mr. Babbage, if you put into the machine wrong figures, will the right answers come out?’ I am not able to rightly apprehend the kind of confusion of ideas that could provoke such a question.” Charles Babbage (1791-1871) Polymorphism is the third essential feature of an object-oriented programming language, after data abstraction and inheritance. It provides another dimension of separation of interface from implementation, to decouple what from how. Polymorphism allows improved code organization and readability as well as the creation of extensible programs that can be “grown” not only during the original creation of the project, but also when new features are desired. Encapsulation creates new data types by combining characteristics and behaviors. Implementation hiding separates the interface from the implementation by making the details private. This sort of mechanical organization makes ready sense to someone with a procedural programming background. But polymorphism deals with decoupling in terms of types. In the last chapter, you saw how inheritance allows the treatment of an object as its own type or its base type. This ability is critical because it allows many types (derived from the same base type) to be treated as if they were one type, and a single piece of code to work on all those different types equally. The polymorphic method call allows one type to express its distinction from another, similar type, as long as they’re both derived from the same base type. This distinction is expressed through differences in behavior of the methods that you can call through the base class. In this chapter, you’ll learn about polymorphism (also called dynamic binding or late binding or run-time binding)starting from the basics, with simple examples that strip away everything but the polymorphic behavior of the program. Upcasting revisited In the last chapter you saw how an object can be used as its own type or as an object of its base type. Taking an object reference and treating it as a reference to its base type is called upcasting because of the way inheritance trees are drawn with the base class at the top. You also saw a problem arise, which is embodied in the following example about musical instruments. First, since several examples play Notes, we should create a separate Note enumeration, in a package:
```java
//: polymorphism/music/Note.java
// Notes to play on musical instruments.
package polymorphism.music;
public enum Note {
MIDDLE_C, C_SHARP, B_FLAT; // Etc.
} ///:~
```

<!--p216-->
enums were introduced in the Initialization & Cleanup chapter. Here, Wind is a type of Instrument; therefore, Wind is inherited from Instrument:
```java
//: polymorphism/music/Instrument.java
package polymorphism.music;
import static net.mindview.util.Print.*;
class Instrument {
public void play(Note n) {
print("Instrument.play()");
}
}
///:~
//: polymorphism/music/Wind.java
package polymorphism.music;
// Wind objects are instruments
// because they have the same interface:
public class Wind extends Instrument {
// Redefine interface method:
public void play(Note n) {
System.out.println("Wind.play() " + n);
}
} ///:~
//: polymorphism/music/Music.java
// Inheritance & upcasting.
package polymorphism.music;
public class Music {
public static void tune(Instrument i) {
// ...
i.play(Note.MIDDLE_C);
}
public static void main(String[] args) {
Wind flute = new Wind();
tune(flute); // Upcasting
}
} /* Output:
Wind.play() MIDDLE_C
*///:~
```
The method Music.tune( ) accepts an Instrument reference, but also anything derived from Instrument. In main( ), you can see this happening as a Wind reference is passed to tune( ), with no cast necessary. This is acceptable—the interface in Instrument must exist in Wind, because Wind is inherited from Instrument. Upcasting from Wind to Instrument may “narrow” that interface, but it cannot make it anything less than the full interface to Instrument. Forgetting the object type Music.java might seem strange to you. Why should anyone intentionally forget the type of an object? This is what happens when you upcast, and it seems like it could be much more straightforward if tune( ) simply takes a Wind reference as its argument. This brings up an essential point: If you did that, you’d need to write a new tune( ) for every type of Instrument in your system. Suppose we follow this reasoning and add Stringed and Brass instruments:

<!--p217-->
```java
//: polymorphism/music/Music2.java
// Overloading instead of upcasting.
package polymorphism.music;
import static net.mindview.util.Print.*;
class Stringed extends Instrument {
public void play(Note n) {
print("Stringed.play() " + n);
}
}
class Brass extends Instrument {
public void play(Note n) {
print("Brass.play() " + n);
}
}
public class Music2 {
public static void tune(Wind i) {
i.play(Note.MIDDLE_C);
}
public static void tune(Stringed i) {
i.play(Note.MIDDLE_C);
}
public static void tune(Brass i) {
i.play(Note.MIDDLE_C);
}
public static void main(String[] args) {
Wind flute = new Wind();
Stringed violin = new Stringed();
Brass frenchHorn = new Brass();
tune(flute); // No upcasting
tune(violin);
tune(frenchHorn);
}
} /* Output:
Wind.play() MIDDLE_C
Stringed.play() MIDDLE_C
Brass.play() MIDDLE_C
*///:~
```

<!--p218-->
This works, but there’s a major drawback: you must write type-specific methods for each new Instrument class you add. This means more programming in the first place, but it also means that if you want to add a new method like tune( ) or a new type of Instrument, you’ve got a lot of work to do. Add the fact that the compiler won’t give you any error messages if you forget to overload one of your methods and the whole process of working with types becomes unmanageable. Wouldn’t it be much nicer if you could just write a single method that takes the base class as its argument, and not any of the specific derived classes? That is, wouldn’t it be nice if you could forget that there are derived classes, and write your code to talk only to the base class? That’s exactly what polymorphism allows you to do. However, most programmers who come from a procedural programming background have a bit of trouble with the way polymorphism works. Exercise 1: (2) Create a Cycle class, with subclasses Unicycle, Bicycle and Tricycle. Demonstrate that an instance of each type can be upcast to Cycle via a ride( ) method. Polymorphism The twist The difficulty with Music.java can be seen by running the program. The output is Wind.play( ). This is clearly the desired output, but it doesn’t seem to make sense that it would work that way. Look at the tune( ) method:
```java
public static void tune(Instrument i) {
// ...
i.play(Note.MIDDLE_C);
}
```

<!--p219-->
It receives an Instrument reference. So how can the compiler possibly know that this Instrument reference points to a Wind in this case and not a Brass or Stringed? The compiler can’t. To get a deeper understanding of the issue, it’s helpful to examine the subject of binding. Method-call binding Connecting a method call to a method body is called binding. When binding is performed before the program is run (by the compiler and linker, if there is one), it’s called early binding. You might not have heard the term before because it has never been an option with procedural languages. C compilers have only one kind of method call, and that’s early binding. The confusing part of the preceding program revolves around early binding, because the compiler cannot know the correct method to call when it has only an Instrument reference. The solution is called late binding, which means that the binding occurs at run time, based on the type of object. Late binding is also called dynamic binding or runtime binding. When a language implements late binding, there must be some mechanism to determine the type of the object at run time and to call the appropriate method. That is, the compiler still doesn’t know the object type, but the method-call mechanism finds out and calls the correct method body. The late-binding mechanism varies from language to language, but you can imagine that some sort of type information must be installed in the objects. All method binding in Java uses late binding unless the method is static or final (private methods are implicitly final). This means that ordinarily you don’t need to make any decisions about whether late binding will occur—it happens automatically. Why would you declare a method final? As noted in the last chapter, it prevents anyone from overriding that method. Perhaps more important, it effectively “turns off” dynamic binding, or rather it tells the compiler that dynamic binding isn’t necessary. This allows the compiler to generate slightly more efficient code for final method calls. However, in most cases it won’t make any overall performance difference in your program, so it’s best to only use final as a design decision, and not as an attempt to improve performance. Producing the right behavior Once you know that all method binding in Java happens polymorphically via late binding, you can write your code to talk to the base class and know that all the derived-class cases will work correctly using the same code. Or to put it another way, you “send a message to an object and let the object figure out the right thing to do.” The classic example in OOP is the “shape” example. This is commonly used because it is easy to visualize, but unfortunately it can confuse novice programmers into thinking that OOP is just for graphics programming, which is of course not the case. The shape example has a base class called Shape and various derived types: Circle, Square, Triangle, etc. The reason the example works so well is that it’s easy to say “a circle is a type of shape” and be understood. The inheritance diagram shows the relationships: The upcast could occur in a statement as simple as:
```java
Shape s = new Circle();
```
Here, a Circle object is created, and the resulting reference is immediately assigned to a Shape, which would seem to be an error (assigning one type to another); and yet it’s fine because a Circleis a Shape by inheritance. So the compiler agrees with the statement and doesn’t issue an error message. Suppose you call one of the base-class methods (that have been overridden in the derived classes):
```java
s.draw();
```
Again, you might expect that Shape’s draw( ) is called because this is, after all, a Shape reference—so how could the compiler know to do anything else? And yet the proper Circle.draw( ) is called because of late binding (polymorphism). The following example puts it a slightly different way. First, let’s create a reusable library of Shape types:
```java
//: polymorphism/shape/Shape.java
package polymorphism.shape;
public class Shape {
public void draw() {}
public void erase() {}
} ///:~
//: polymorphism/shape/Circle.java
package polymorphism.shape;
import static net.mindview.util.Print.*;
public class Circle extends Shape {
```

<!--p220-->
Polymorphism

<!--p221-->
```java
public void draw() { print("Circle.draw()"); }
public void erase() { print("Circle.erase()"); }
} ///:~
//: polymorphism/shape/Square.java
package polymorphism.shape;
import static net.mindview.util.Print.*;
public class Square extends Shape {
public void draw() { print("Square.draw()"); }
public void erase() { print("Square.erase()"); }
} ///:~
//: polymorphism/shape/Triangle.java
package polymorphism.shape;
import static net.mindview.util.Print.*;
public class Triangle extends Shape {
public void draw() { print("Triangle.draw()"); }
public void erase() { print("Triangle.erase()"); }
} ///:~
//: polymorphism/shape/RandomShapeGenerator.java
// A "factory" that randomly creates shapes.
package polymorphism.shape;
import java.util.*;
public class RandomShapeGenerator {
private Random rand = new Random(47);
public Shape next() {
switch(rand.nextInt(3)) {
default:
case 0: return new Circle();
case 1: return new Square();
case 2: return new Triangle();
}
}
} ///:~
//: polymorphism/Shapes.java
// Polymorphism in Java.
import polymorphism.shape.*;
public class Shapes {
private static RandomShapeGenerator gen =
new RandomShapeGenerator();
public static void main(String[] args) {
Shape[] s = new Shape[9];
// Fill up the array with shapes:
for(int i = 0; i < s.length; i++)
s[i] = gen.next();
// Make polymorphic method calls:
for(Shape shp : s)
shp.draw();
}
} /* Output:
Triangle.draw()
Triangle.draw()
Square.draw()
Triangle.draw()
Square.draw()
Triangle.draw()
Square.draw()
Triangle.draw()
Circle.draw()
*///:~
```

<!--p222-->
The base class Shape establishes the common interface to anything inherited from Shape— that is, all shapes can be drawn and erased. The derived classes override these definitions to provide unique behavior for each specific type of shape. RandomShapeGenerator is a kind of “factory” that produces a reference to a randomly- selected Shape object each time you call its next( ) method. Note that the upcasting happens in the return statements, each of which takes a reference to a Circle, Square, or Triangle and sends it out of next( ) as the return type, Shape. So whenever you call next( ), you never get a chance to see what specific type it is, since you always get back a plain Shape reference. main( ) contains an array of Shape references filled through calls to RandomShapeGenerator.next( ). At this point you know you have Shapes, but you don’t know anything more specific than that (and neither does the compiler). However, when you step through this array and call draw( ) for each one, the correct type-specific behavior magically occurs, as you can see from the output when you run the program. The point of creating the shapes randomly is to drive home the understanding that the compiler can have no special knowledge that allows it to make the correct calls at compile time. All the calls to draw( ) must be made through dynamic binding. Exercise 2: (1) Add the @Override annotation to the shapes example. Exercise 3: (1) Add a new method in the base class of Shapes.java that prints a message, but don’t override it in the derived classes. Explain what happens. Now override it in one of the derived classes but not the others, and see what happens. Finally, override it in all the derived classes. Exercise 4: (2) Add a new type of Shape to Shapes.java and verify in main( ) that polymorphism works for your new type as it does in the old types. Exercise 5: (1) Starting from Exercise 1, add a wheels( ) method in Cycle, which returns the number of wheels. Modify ride( ) to call wheels( ) and verify that polymorphism works. Extensibility Now let’s return to the musical instrument example. Because of polymorphism, you can add as many new types as you want to the system without changing the tune( ) method. In a well-designed OOP program, most or all of your methods will follow the model of tune( ) and communicate only with the base-class interface. Such a program is extensible because you can add new functionality by inheriting new data types from the common base class. The methods that manipulate the base-class interface will not need to be changed at all to accommodate the new classes. Consider what happens if you take the instrument example and add more methods in the base class and a number of new classes. Here’s the diagram: Polymorphism All these new classes work correctly with the old, unchanged tune( ) method. Even if tune( ) is in a separate file and new methods are added to the interface of Instrument, tune( ) will still work correctly, even without recompiling it. Here is the implementation of the diagram:

<!--p223-->
```java
//: polymorphism/music3/Music3.java
// An extensible program.
package polymorphism.music3;
import polymorphism.music.Note;
import static net.mindview.util.Print.*;
class Instrument {
void play(Note n) { print("Instrument.play() " + n); }
String what() { return "Instrument"; }
void adjust() { print("Adjusting Instrument"); }
}
class Wind extends Instrument {
void play(Note n) { print("Wind.play() " + n); }
String what() { return "Wind"; }
void adjust() { print("Adjusting Wind"); }
}
class Percussion extends Instrument {
void play(Note n) { print("Percussion.play() " + n); }
String what() { return "Percussion"; }
void adjust() { print("Adjusting Percussion"); }
}
class Stringed extends Instrument {
void play(Note n) { print("Stringed.play() " + n); }
String what() { return "Stringed"; }
void adjust() { print("Adjusting Stringed"); }
}
class Brass extends Wind {
void play(Note n) { print("Brass.play() " + n); }
void adjust() { print("Adjusting Brass"); }
}
class Woodwind extends Wind {
void play(Note n) { print("Woodwind.play() " + n); }
String what() { return "Woodwind"; }
}
public class Music3 {
// Doesn’t care about type, so new types
// added to the system still work right:
public static void tune(Instrument i) {
// ...
i.play(Note.MIDDLE_C);
}
public static void tuneAll(Instrument[] e) {
for(Instrument i : e)
tune(i);
}
public static void main(String[] args) {
// Upcasting during addition to the array:
Instrument[] orchestra = {
new Wind(),
new Percussion(),
new Stringed(),
new Brass(),
new Woodwind()
};
tuneAll(orchestra);
}
} /* Output:
Wind.play() MIDDLE_C
Percussion.play() MIDDLE_C
Stringed.play() MIDDLE_C
Brass.play() MIDDLE_C
Woodwind.play() MIDDLE_C
*///:~
```

<!--p224-->
The new methods are what( ), which returns a String reference with a description of the class, and adjust( ), which provides some way to adjust each instrument. In main( ), when you place something inside the orchestra array, you automatically upcast to Instrument. You can see that the tune( ) method is blissfully ignorant of all the code changes that have happened around it, and yet it works correctly. This is exactly what polymorphism is supposed to provide. Changes in your code don’t cause damage to parts of the program that should not be affected. Put another way, polymorphism is an important technique for the programmer to “separate the things that change from the things that stay the same.” Polymorphism Exercise 6: (1) Change Music3.java so that what( ) becomes the root Object method toString( ). Try printing the Instrument objects using System.out.println( ) (without any casting). Exercise 7: (2) Add a new type of Instrument to Music3.java and verify that polymorphism works for your new type. Exercise 8: (2) Modify Music3.java so that it randomly creates Instrument objects the way Shapes.java does. Exercise 9: (3) Create an inheritance hierarchy of Rodent: Mouse, Gerbil, Hamster, etc. In the base class, provide methods that are common to all Rodents, and override these in the derived classes to perform different behaviors depending on the specific type of Rodent. Create an array of Rodent, fill it with different specific types of Rodents, and call your base-class methods to see what happens. Exercise 10: (3) Create a base class with two methods. In the first method, call the second method. Inherit a class and override the second method. Create an object of the derived class, upcast it to the base type, and call the first method. Explain what happens.
## Pitfall: “overriding” private methods
Here’s something you might innocently try to do:
```java
//: polymorphism/PrivateOverride.java
// Trying to override a private method.
package polymorphism;
import static net.mindview.util.Print.*;
public class PrivateOverride {
private void f() { print("private f()"); }
public static void main(String[] args) {
PrivateOverride po = new Derived();
po.f();
}
}
class Derived extends PrivateOverride {
public void f() { print("public f()"); }
} /* Output:
private f()
*///:~
```

<!--p225-->
You might reasonably expect the output to be “public f( )”, but a private method is automatically final, and is also hidden from the derived class. So Derived’s f( ) in this case is a brand new method; it’s not even overloaded, since the base-class version of f( ) isn’t visible in Derived. The result of this is that only non-private methods may be overridden, but you should watch out for the appearance of overriding private methods, which generates no compiler warnings, but doesn’t do what you might expect. To be clear, you should use a different name from a private base-class method in your derived class. Polymorphism
## Pitfall: fields and static methods
Once you learn about polymorphism, you can begin to think that everything happens polymorphically. However, only ordinary method calls can be polymorphic. For example, if you access a field directly, that access will be resolved at compile time, as the following example demonstrates:1
```java
//: polymorphism/FieldAccess.java
// Direct field access is determined at compile time.
class Super {
public int field = 0;
public int getField() { return field; }
}
class Sub extends Super {
public int field = 1;
public int getField() { return field; }
public int getSuperField() { return super.field; }
}
public class FieldAccess {
public static void main(String[] args) {
Super sup = new Sub(); // Upcast
System.out.println("sup.field = " + sup.field +
", sup.getField() = " + sup.getField());
Sub sub = new Sub();
System.out.println("sub.field = " +
sub.field + ", sub.getField() = " +
sub.getField() +
", sub.getSuperField() = " +
sub.getSuperField());
}
} /* Output:
sup.field = 0, sup.getField() = 1
sub.field = 1, sub.getField() = 1, sub.getSuperField() = 0
*///:~
```
When a Sub object is upcast to a Super reference, any field accesses are resolved by the compiler, and are thus not polymorphic. In this example, different storage is allocated for Super.field and Sub.field. Thus, Sub actually contains two fields called field: its own and the one that it gets from Super. However, the Super version is not the default that is produced when you refer to field in Sub; in order to get the Super field you must explicitly say super.field. Although this seems like it could be a confusing issue, in practice it virtually never comes up. For one thing, you’ll generally make all fields private and so you won’t access them directly, but only as side effects of calling methods. In addition, you probably won’t give the same name to a base-class field and a derived-class field, because its confusing. If a method is static, it doesn’t behave polymorphically:
```java
//: polymorphism/StaticPolymorphism.java
// Static methods are not polymorphic.
class StaticSuper {
public static String staticGet() {
```

<!--p226-->
1Thanks to Randy Nichols for asking this question.
```java
return "Base staticGet()";
}
public String dynamicGet() {
return "Base dynamicGet()";
}
}
class StaticSub extends StaticSuper {
public static String staticGet() {
return "Derived staticGet()";
}
public String dynamicGet() {
return "Derived dynamicGet()";
}
}
public class StaticPolymorphism {
public static void main(String[] args) {
StaticSuper sup = new StaticSub(); // Upcast
System.out.println(sup.staticGet());
System.out.println(sup.dynamicGet());
}
} /* Output:
Base staticGet()
Derived dynamicGet()
*///:~
```

<!--p227-->
static methods are associated with the class, and not the individual objects. Constructors and polymorphism As usual, constructors are different from other kinds of methods. This is also true when polymorphism is involved. Even though constructors are not polymorphic (they’re actually static methods, but the static declaration is implicit), it’s important to understand the way constructors work in complex hierarchies and with polymorphism. This understanding will help you avoid unpleasant entanglements. Order of constructor calls The order of constructor calls was briefly discussed in the Initialization & Cleanup chapter and again in the Reusing Classes chapter, but that was before polymorphism was introduced. A constructor for the base class is always called during the construction process for a derived class, chaining up the inheritance hierarchy so that a constructor for every base class is called. This makes sense because the constructor has a special job: to see that the object is built properly. A derived class has access to its own members only, and not to those of the base class (whose members are typically private). Only the base-class constructor has the proper knowledge and access to initialize its own elements. Therefore, it’s essential that all constructors get called; otherwise the entire object wouldn’t be constructed. That’s why the compiler enforces a constructor call for every portion of a derived class. It will silently call the default constructor if you don’t explicitly call a base-class constructor in the derived-class constructor body. If there is no default constructor, the compiler will complain. (In the case where a class has no constructors, the compiler will automatically synthesize a default constructor.) Let’s take a look at an example that shows the effects of composition, inheritance, and polymorphism on the order of construction:
```java
//: polymorphism/Sandwich.java
// Order of constructor calls.
package polymorphism;
import static net.mindview.util.Print.*;
class Meal {
Meal() { print("Meal()"); }
}
class Bread {
Bread() { print("Bread()"); }
}
class Cheese {
Cheese() { print("Cheese()"); }
}
class Lettuce {
Lettuce() { print("Lettuce()"); }
}
class Lunch extends Meal {
Lunch() { print("Lunch()"); }
}
class PortableLunch extends Lunch {
PortableLunch() { print("PortableLunch()");}
}
public class Sandwich extends PortableLunch {
private Bread b = new Bread();
private Cheese c = new Cheese();
private Lettuce l = new Lettuce();
public Sandwich() { print("Sandwich()"); }
public static void main(String[] args) {
new Sandwich();
}
} /* Output:
Meal()
Lunch()
PortableLunch()
Bread()
Cheese()
Lettuce()
Sandwich()
*///:~
```

<!--p228-->
This example creates a complex class out of other classes, and each class has a constructor that announces itself. The important class is Sandwich, which reflects three levels of inheritance (four, if you count the implicit inheritance from Object) and three member objects. You can see the output when a Sandwich object is created in main( ). This means that the order of constructor calls for a complex object is as follows: 1.The base-class constructor is called. This step is repeated recursively such that the root of the hierarchy is constructed first, followed by the next-derived class, etc., until the most-derived class is reached. 2.Member initializers are called in the order of declaration. Polymorphism 3.The body of the derived-class constructor is called. The order of the constructor calls is important. When you inherit, you know all about the base class and can access any public and protected members of the base class. This means that you must be able to assume that all the members of the base class are valid when you’re in the derived class. In a normal method, construction has already taken place, so all the members of all parts of the object have been built. Inside the constructor, however, you must be able to assume that all members that you use have been built. The only way to guarantee this is for the base-class constructor to be called first. Then when you’re in the derived-class constructor, all the members you can access in the base class have been initialized. Knowing that all members are valid inside the constructor is also the reason that, whenever possible, you should initialize all member objects (that is, objects placed in the class using composition) at their point of definition in the class (e.g., b, c, and l in the preceding example). If you follow this practice, you will help ensure that all base class members and member objects of the current object have been initialized. Unfortunately, this doesn’t handle every case, as you will see in the next section. Exercise 11: (1) Add class Pickle to Sandwich.java. Inheritance and cleanup When using composition and inheritance to create a new class, most of the time you won’t have to worry about cleaning up; subobjects can usually be left to the garbage collector. If you do have cleanup issues, you must be diligent and create a dispose( ) method (the name I have chosen to use here; you may come up with something better) for your new class. And with inheritance, you must override dispose( ) in the derived class if you have any special cleanup that must happen as part of garbage collection. When you override dispose( ) in an inherited class, it’s important to remember to call the base-class version of dispose( ), since otherwise the base-class cleanup will not happen. The following example demonstrates this:

<!--p229-->
```java
//: polymorphism/Frog.java
// Cleanup and inheritance.
package polymorphism;
import static net.mindview.util.Print.*;
class Characteristic {
private String s;
Characteristic(String s) {
this.s = s;
print("Creating Characteristic " + s);
}
protected void dispose() {
print("disposing Characteristic " + s);
}
}
class Description {
private String s;
Description(String s) {
this.s = s;
print("Creating Description " + s);
}
protected void dispose() {
print("disposing Description " + s);
}
}
class LivingCreature {
private Characteristic p =
new Characteristic("is alive");
private Description t =
new Description("Basic Living Creature");
LivingCreature() {
print("LivingCreature()");
}
protected void dispose() {
print("LivingCreature dispose");
t.dispose();
p.dispose();
}
}
class Animal extends LivingCreature {
private Characteristic p =
new Characteristic("has heart");
private Description t =
new Description("Animal not Vegetable");
Animal() { print("Animal()"); }
protected void dispose() {
print("Animal dispose");
t.dispose();
p.dispose();
super.dispose();
}
}
class Amphibian extends Animal {
private Characteristic p =
new Characteristic("can live in water");
private Description t =
new Description("Both water and land");
Amphibian() {
print("Amphibian()");
}
protected void dispose() {
print("Amphibian dispose");
t.dispose();
p.dispose();
super.dispose();
}
}
public class Frog extends Amphibian {
private Characteristic p = new Characteristic("Croaks");
private Description t = new Description("Eats Bugs");
public Frog() { print("Frog()"); }
protected void dispose() {
print("Frog dispose");
t.dispose();
p.dispose();
super.dispose();
}
public static void main(String[] args) {
Frog frog = new Frog();
print("Bye!");
frog.dispose();
}
} /* Output:
Creating Characteristic is alive
Creating Description Basic Living Creature
```

<!--p230-->
Polymorphism
```java
LivingCreature()
Creating Characteristic has heart
Creating Description Animal not Vegetable
Animal()
Creating Characteristic can live in water
Creating Description Both water and land
Amphibian()
Creating Characteristic Croaks
Creating Description Eats Bugs
Frog()
Bye!
Frog dispose
disposing Description Eats Bugs
disposing Characteristic Croaks
Amphibian dispose
disposing Description Both water and land
disposing Characteristic can live in water
Animal dispose
disposing Description Animal not Vegetable
disposing Characteristic has heart
LivingCreature dispose
disposing Description Basic Living Creature
disposing Characteristic is alive
*///:~
```
Each class in the hierarchy also contains a member objects of types Characteristic and Description, which must also be disposed. The order of disposal should be the reverse of the order of initialization, in case one subobject is dependent on another. For fields, this means the reverse of the order of declaration (since fields are initialized in declaration order). For base classes (following the form that’s used in C++ for destructors), you should perform the derived-class cleanup first, then the base-class cleanup. That’s because the derived-class cleanup could call some methods in the base class that require the base-class components to be alive, so you must not destroy them prematurely. From the output you can see that all parts of the Frog object are disposed in reverse order of creation. From this example, you can see that although you don’t always need to perform cleanup, when you do, the process requires care and awareness. Exercise 12: (3) Modify Exercise 9 so that it demonstrates the order of initialization of the base classes and derived classes. Now add member objects to both the base and derived classes and show the order in which their initialization occurs during construction. Also note that in the above example, a Frog object “owns” its member objects. It creates them, and it knows how long they should live (as long as the Frog does), so it knows when to dispose( ) the member objects. However, if one of these member objects is shared with one or more other objects, the problem becomes more complex and you cannot simply assume that you can call dispose( ). In this case, reference counting may be necessary to keep track of the number of objects that are still accessing a shared object. Here’s what it looks like:

<!--p231-->
```java
//: polymorphism/ReferenceCounting.java
// Cleaning up shared member objects.
import static net.mindview.util.Print.*;
class Shared {
private int refcount = 0;
private static long counter = 0;
private final long id = counter++;
public Shared() {
print("Creating " + this);
}
public void addRef() { refcount++; }
protected void dispose() {
if(--refcount == 0)
print("Disposing " + this);
}
public String toString() { return "Shared " + id; }
}
class Composing {
private Shared shared;
private static long counter = 0;
private final long id = counter++;
public Composing(Shared shared) {
print("Creating " + this);
this.shared = shared;
this.shared.addRef();
}
protected void dispose() {
print("disposing " + this);
shared.dispose();
}
public String toString() { return "Composing " + id; }
}
public class ReferenceCounting {
public static void main(String[] args) {
Shared shared = new Shared();
Composing[] composing = { new Composing(shared),
new Composing(shared), new Composing(shared),
new Composing(shared), new Composing(shared) };
for(Composing c : composing)
c.dispose();
}
} /* Output:
Creating Shared 0
Creating Composing 0
Creating Composing 1
Creating Composing 2
Creating Composing 3
Creating Composing 4
disposing Composing 0
disposing Composing 1
disposing Composing 2
disposing Composing 3
disposing Composing 4
Disposing Shared 0
*///:~
```

<!--p232-->
The static long counter keeps track of the number of instances of Shared that are created, and it also provides a value for id. The type of counter is long rather than int, to prevent overflow (this is just good practice; overflowing such a counter is not likely to happen in any of the examples in this book). The id is final because we do not expect it to change its value during the lifetime of the object. When you attach a shared object to your class, you must remember to call addRef( ), but the dispose( ) method will keep track of the reference count and decide when to actually perform the cleanup. This technique requires extra diligence to use, but if you are sharing objects that require cleanup you don’t have much choice. Exercise 13: (3) Add a finalize( ) method to ReferenceCounting.java to verify the termination condition (see the Initialization & Cleanup chapter). Polymorphism Exercise 14: (4) Modify Exercise 12 so that one of the member objects is a shared object with reference counting, and demonstrate that it works properly. Behavior of polymorphic methods inside constructors The hierarchy of constructor calls brings up an interesting dilemma. What happens if you’re inside a constructor and you call a dynamically-bound method of the object being constructed? Inside an ordinary method, the dynamically-bound call is resolved at run time, because the object cannot know whether it belongs to the class that the method is in or some class derived from it. If you call a dynamically-bound method inside a constructor, the overridden definition for that method is used. However, the effect of this call can be rather unexpected because the overridden method will be called before the object is fully constructed. This can conceal some difficult-to-find bugs. Conceptually, the constructor’s job is to bring the object into existence (which is hardly an ordinary feat). Inside any constructor, the entire object might be only partially formed—you can only know that the base-class objects have been initialized. If the constructor is only one step in building an object of a class that’s been derived from that constructor’s class, the derived parts have not yet been initialized at the time that the current constructor is being called. A dynamically bound method call, however, reaches “outward” into the inheritance hierarchy. It calls a method in a derived class. If you do this inside a constructor, you call a method that might manipulate members that haven’t been initialized yet—a sure recipe for disaster. You can see the problem in the following example:

<!--p233-->
```java
//: polymorphism/PolyConstructors.java
// Constructors and polymorphism
// don’t produce what you might expect.
import static net.mindview.util.Print.*;
class Glyph {
void draw() { print("Glyph.draw()"); }
Glyph() {
print("Glyph() before draw()");
draw();
print("Glyph() after draw()");
}
}
class RoundGlyph extends Glyph {
private int radius = 1;
RoundGlyph(int r) {
radius = r;
print("RoundGlyph.RoundGlyph(), radius = " + radius);
}
void draw() {
print("RoundGlyph.draw(), radius = " + radius);
}
}
public class PolyConstructors {
public static void main(String[] args) {
new RoundGlyph(5);
}
} /* Output:
Glyph() before draw()
RoundGlyph.draw(), radius = 0
Glyph() after draw()
RoundGlyph.RoundGlyph(), radius = 5
*///:~
```
Glyph. draw( ) is designed to be overridden, which happens in RoundGlyph. But the Glyph constructor calls this method, and the call ends up in RoundGlyph.draw( ), which would seem to be the intent. But if you look at the output, you can see that when Glyph’s constructor calls draw( ), the value of radius isn’t even the default initial value 1. It’s 0. This would probably result in either a dot or nothing at all being drawn on the screen, and you’d be left staring, trying to figure out why the program won’t work. The order of initialization described in the earlier section isn’t quite complete, and that’s the key to solving the mystery. The actual process of initialization is: 1.The storage allocated for the object is initialized to binary zero before anything else happens. 2.The base-class constructors are called as described previously. At this point, the overridden draw( ) method is called (yes, before the RoundGlyph constructor is called), which discovers a radius value of zero, due to Step 1. 3.Member initializers are called in the order of declaration. 4.The body of the derived-class constructor is called. There’s an upside to this, which is that everything is at least initialized to zero (or whatever zero means for that particular data type) and not just left as garbage. This includes object references that are embedded inside a class via composition, which become null. So if you forget to initialize that reference, you’ll get an exception at run time. Everything else gets zero, which is usually a telltale value when looking at output. On the other hand, you should be pretty horrified at the outcome of this program. You’ve done a perfectly logical thing, and yet the behavior is mysteriously wrong, with no complaints from the compiler. (C++ produces more rational behavior in this situation.) Bugs like this could easily be buried and take a long time to discover. As a result, a good guideline for constructors is, “Do as little as possible to set the object into a good state, and if you can possibly avoid it, don’t call any other methods in this class.” The only safe methods to call inside a constructor are those that are final in the base class. (This also applies to private methods, which are automatically final.) These cannot be overridden and thus cannot produce this kind of surprise. You may not always be able to follow this guideline, but it’s something to strive towards. Exercise 15: (2) Add a RectangularGlyph to PolyConstructors.java and demonstrate the problem described in this section. Covariant return types Java SE5 adds covariant return types, which means that an overridden method in a derived class can return a type derived from the type returned by the base-class method:
```java
//: polymorphism/CovariantReturn.java
```

<!--p234-->
Polymorphism
```java
class Grain {
public String toString() { return "Grain"; }
}
class Wheat extends Grain {
public String toString() { return "Wheat"; }
}
class Mill {
Grain process() { return new Grain(); }
}
class WheatMill extends Mill {
Wheat process() { return new Wheat(); }
}
public class CovariantReturn {
public static void main(String[] args) {
Mill m = new Mill();
Grain g = m.process();
System.out.println(g);
m = new WheatMill();
g = m.process();
System.out.println(g);
}
} /* Output:
Grain
Wheat
*///:~
```
The key difference between Java SE5 and earlier versions of java is that the earlier versions would force the overridden version of process( ) to return Grain, rather than Wheat, even though Wheat is derived from Grain and thus is still a legitimate return type. Covariant return types allow the more specific Wheat return type. Designing with inheritance Once you learn about polymorphism, it can seem that everything ought to be inherited, because polymorphism is such a clever tool. This can burden your designs; in fact, if you choose inheritance first when you’re using an existing class to make a new class, things can become needlessly complicated. A better approach is to choose composition first, especially when it’s not obvious which one you should use. Composition does not force a design into an inheritance hierarchy. But composition is also more flexible since it’s possible to dynamically choose a type (and thus behavior) when using composition, whereas inheritance requires an exact type to be known at compile time. The following example illustrates this:

<!--p235-->
```java
//: polymorphism/Transmogrify.java
// Dynamically changing the behavior of an object
// via composition (the "State" design pattern).
import static net.mindview.util.Print.*;
class Actor {
public void act() {}
}
class HappyActor extends Actor {
public void act() { print("HappyActor"); }
}
class SadActor extends Actor {
public void act() { print("SadActor"); }
}
class Stage {
private Actor actor = new HappyActor();
public void change() { actor = new SadActor(); }
public void performPlay() { actor.act(); }
}
public class Transmogrify {
public static void main(String[] args) {
Stage stage = new Stage();
stage.performPlay();
stage.change();
stage.performPlay();
}
} /* Output:
HappyActor
SadActor
*///:~
```

<!--p236-->

<!--p237-->

<!--p238-->
A Stage object contains a reference to an Actor, which is initialized to a HappyActor object. This means performPlay( ) produces a particular behavior. But since a reference can be rebound to a different object at run time, a reference for a SadActor object can be substituted in actor, and then the behavior produced by performPlay( ) changes. Thus you gain dynamic flexibility at run time. (This is also called the State Pattern. See Thinking in Patterns (with Java) at www.MindView.com.) In contrast, you can’t decide to inherit differently at run time; that must be completely determined at compile time. A general guideline is “Use inheritance to express differences in behavior, and fields to express variations in state.” In the preceding example, both are used; two different classes are inherited to express the difference in the act( ) method, and Stage uses composition to allow its state to be changed. In this case, that change in state happens to produce a change in behavior. Exercise 16: (3) Following the example in Transmogrify.java, create a Starship class containing an AlertStatus reference that can indicate three different states. Include methods to change the states. Substitution vs. extension It would seem that the cleanest way to create an inheritance hierarchy is to take the “pure” approach. That is, only methods that have been established in the base class are overridden in the derived class, as seen in this diagram: Polymorphism This can be called a pure “is-a” relationship because the interface of a class establishes what it is. Inheritance guarantees that any derived class will have the interface of the base class and nothing less. If you follow this diagram, derived classes will also have no more than the base-class interface. This can be thought of as pure substitution, because derived class objects can be perfectly substituted for the base class, and you never need to know any extra information about the subclasses when you’re using them: That is, the base class can receive any message you can send to the derived class because the two have exactly the same interface. All you need to do is upcast from the derived class and never look back to see what exact type of object you’re dealing with. Everything is handled through polymorphism. When you see it this way, it seems like a pure is-a relationship is the only sensible way to do things, and any other design indicates muddled thinking and is by definition broken. This too is a trap. As soon as you start thinking this way, you’ll turn around and discover that extending the interface (which, unfortunately, the keyword extends seems to encourage) is the perfect solution to a particular problem. This can be termed an “is-like-a” relationship, because the derived class is like the base class—it has the same fundamental interface—but it has other features that require additional methods to implement: While this is also a useful and sensible approach (depending on the situation), it has a drawback. The extended part of the interface in the derived class is not available from the base class, so once you upcast, you can’t call the new methods: If you’re not upcasting in this case, it won’t bother you, but often you’ll get into a situation in which you need to rediscover the exact type of the object so you can access the extended methods of that type. The following section shows how this is done. Downcasting and runtime type information Since you lose the specific type information via an upcast (moving up the inheritance hierarchy), it makes sense that to retrieve the type information—that is, to move back down the inheritance hierarchy—you use a downcast. However, you know an upcast is always safe because the base class cannot have a bigger interface than the derived class. Therefore, every message you send through the base class interface is guaranteed to be accepted. But with a downcast, you don’t really know that a shape (for example) is actually a circle. It could instead be a triangle or square or some other type. To solve this problem, there must be some way to guarantee that a downcast is correct, so that you won’t accidentally cast to the wrong type and then send a message that the object can’t accept. This would be quite unsafe. In some languages (like C++) you must perform a special operation in order to get a type-safe downcast, but in Java, every cast is checked! So even though it looks like you’re just performing an ordinary parenthesized cast, at run time this cast is checked to ensure that it is in fact the type you think it is. If it isn’t, you get a ClassCastException. This act of checking Polymorphism types at run time is called runtime type identification (RTTI). The following example demonstrates the behavior of RTTI:
```java
//: polymorphism/RTTI.java
// Downcasting & Runtime type information (RTTI).
// {ThrowsException}
class Useful {
public void f() {}
public void g() {}
}
class MoreUseful extends Useful {
public void f() {}
public void g() {}
public void u() {}
public void v() {}
public void w() {}
}
public class RTTI {
public static void main(String[] args) {
Useful[] x = {
new Useful(),
new MoreUseful()
};
x[0].f();
x[1].g();
// Compile time: method not found in Useful:
//! x[1].u();
((MoreUseful)x[1]).u(); // Downcast/RTTI
((MoreUseful)x[0]).u(); // Exception thrown
}
} ///:~
```

<!--p239-->
As in the previous diagram, MoreUseful extends the interface of Useful. But since it’s inherited, it can also be upcast to a Useful. You can see this happening in the initialization of the array x in main( ). Since both objects in the array are of class Useful, you can send the f( ) and g( ) methods to both, and if you try to call u( ) (which exists only in MoreUseful), you’ll get a compile-time error message. If you want to access the extended interface of a MoreUseful object, you can try to downcast. If it’s the correct type, it will be successful. Otherwise, you’ll get a ClassCastException. You don’t need to write any special code for this exception, since it indicates a programmer error that could happen anywhere in a program. The {ThrowsException} comment tag tells this book’s build system to expect this program to throw an exception when it executes. There’s more to RTTI than a simple cast. For example, there’s a way to see what type you’re dealing with before you try to downcast it. All of the Type Information chapter is devoted to the study of different aspects of Java run-time type identification. Exercise 17: (2) Using the Cycle hierarchy from Exercise 1, add a balance( ) method to Unicycle and Bicycle, but not to Tricycle. Create instances of all three types and upcast them to an array of Cycle. Try to call balance( ) on each element of the array and observe the results. Downcast and call balance( ) and observe what happens. Polymorphism Summary Polymorphism means “different forms.” In object-oriented programming, you have the same interface from the base class, and different forms using that interface: the different versions of the dynamically bound methods. You’ve seen in this chapter that it’s impossible to understand, or even create, an example of polymorphism without using data abstraction and inheritance. Polymorphism is a feature that cannot be viewed in isolation (like a switch statement can, for example), but instead works only in concert, as part of the larger picture of class relationships. To use polymorphism—and thus object-oriented techniques—effectively in your programs, you must expand your view of programming to include not just members and messages of an individual class, but also the commonality among classes and their relationships with each other. Although this requires significant effort, it’s a worthy struggle. The results are faster program development, better code organization, extensible programs, and easier code maintenance. Solutions to selected exercises can be found in the electronic document The Thinking in Java Annotated Solution Guide, available for sale from www.MindView.net.