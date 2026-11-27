# 14. Type Information (printed p393-438)


<!--p415-->
Type Information Runtime type information (RTTI) allows you to discover and use type information while a program is running. It frees you from the constraint of doing type-oriented things only at compile time, and can enable some very powerful programs. The need for RTTI uncovers a plethora of interesting (and often perplexing) 0 0 design issues, and raises fundamental questions about how you should structure your programs. This chapter looks at the ways that Java allows you to discover information about objects and classes at run time. This takes two forms: "traditional" RTTI, which assumes that you have all the types available at compile time, and the reflection mechanism, which allows you to discover and use class information solely at run time. The need for RTTI Consider the now-familiar example of a class hierarchy that uses polymorphism. The generic type is the base class Shape, and the specific derived types are Circle, Square, and Triangle: This is a typical class hierarchy diagram, with the base class at the top and the derived classes growing downward. The normal goal in object-oriented programming is for your code to manipulate references to the base type (Shape, in this case), so if you decide to extend the program by adding a new class (such as Rhomboid, derived from Shape), the bulk of the code is not affected. In this example, the dynamically bound method in the Shape interface is draw( ), so the intent is for the client programmer to call draw( ) through a generic Shape reference. In all of the derived classes, draw( ) is overridden, and because it is a dynamically bound method, the proper behavior will occur even though it is called through a generic Shape reference. That’s polymorphism. Thus, you generally create a specific object (Circle, Square, or Triangle), upcast it to a Shape (forgetting the specific type of the object), and use that anonymous Shape reference in the rest of the program. You might code the Shape hierarchy as follows:

<!--p416-->
```java
//: typeinfo/Shapes.java
import java.util.*;
abstract class Shape {
void draw() { System.out.println(this + ".draw()"); }
abstract public String toString();
}
class Circle extends Shape {
public String toString() { return "Circle"; }
}
class Square extends Shape {
public String toString() { return "Square"; }
}
class Triangle extends Shape {
public String toString() { return "Triangle"; }
}
public class Shapes {
public static void main(String[] args) {
List<Shape> shapeList = Arrays.asList(
new Circle(), new Square(), new Triangle()
);
for(Shape shape : shapeList)
shape.draw();
}
} /* Output:
Circle.draw()
Square.draw()
Triangle.draw()
*///:~
```

<!--p417-->
The base class contains a draw( ) method that indirectly uses toString( ) to print an identifier for the class by passing this to System.out.println( ) (notice that toString( ) is declared abstract to force inheritors to override it, and to prevent the instantiation of a plain Shape). If an object appears in a string concatenation expression (involving ‘+’ and String objects), the toString( ) method is automatically called to produce a String representation for that object. Each of the derived classes overrides the toString( ) method (from Object)so that draw( ) ends up (polymorphically) printing something different in each case. In this example, the upcast occurs when the shape is placed into the List<Shape>. During the upcast to Shape, the fact that the objects are specific types of Shape is lost. To the array, they are just Shapes. At the point that you fetch an element out of the array, the container—which is actually holding everything as an Object—automatically casts the result back to a Shape. This is the most basic form of RTTI, because all casts are checked at run time for correctness. That’s what RTTI means: At run time, the type of an object is identified. In this case, the RTTI cast is only partial: The Object is cast to a Shape, and not all the way to a Circle, Square, or Triangle. That’s because the only thing you know at this point is that the List<Shape> is full of Shapes. At compile time, this is enforced by the container and the Java generic system, but at run time the cast ensures it. Now polymorphism takes over and the exact code that’s executed for the Shape is determined by whether the reference is for a Circle, Square, or Triangle. And in general, this is how it should be; you want the bulk of your code to know as little as possible about specific types of objects, and to just deal with the general representation of a family of objects (in this case, Shape). As a result, your code will be easier to write, read, and maintain, and your designs will be easier to implement, understand, and change. So polymorphism is a general goal in object-oriented programming. But what if you have a special programming problem that’s easiest to solve if you know the exact type of a generic reference? For example, suppose you want to allow your users to highlight all the shapes of any particular type by turning them a special color. This way, they can find all the triangles on the screen by highlighting them. Or perhaps your method needs to "rotate" a list of shapes, but it makes no sense to rotate a circle so you’d like to skip the circles. With RTTI, you can ask a Shape reference the exact type that it’s referring to, and thus select and isolate special cases.
## The Class object
To understand how RTTI works in Java, you must first know how type information is represented at run time. This is accomplished through a special kind of object called the Class object, which contains information about the class. In fact, the Class object is used to create all of the "regular" objects of your class. Java performs its RTTI using the Class object, even if you’re doing something like a cast. The class Class also has a number of other ways you can use RTTI. There’s one Class object for each class that is part of your program. That is, each time you write and compile a new class, a single Class object is also created (and stored, appropriately enough, in an identically named .class file). To make an object of that class, the Java Virtual Machine (JVM) that’s executing your program uses a subsystem called a class loader. The class loader subsystem can actually comprise a chain of class loaders, but there’s only one primordial class loader, which is part of the JVM implementation. The primordial class loader loads so-called trusted classes, including Java API classes, typically from the local disk. It’s usually not necessary to have additional class loaders in the chain, but if you have special needs (such as loading classes in a special way to support Web server applications, or downloading classes across a network), then you have a way to hook in additional class loaders. All classes are loaded into the JVM dynamically, upon the first use of a class. This happens when the program makes the first reference to a static member of that class. It turns out that the constructor is also a static method of a class, even though the static keyword is not used for a constructor. Therefore, creating a new object of that class using the new operator also counts as a reference to a static member of the class. Thus, a Java program isn’t completely loaded before it begins, but instead pieces of it are loaded when necessary. This is different from many traditional languages. Dynamic loading enables behavior that is difficult or impossible to duplicate in a statically loaded language like C++. The class loader first checks to see if the Class object for that type is loaded. If not, the default class loader finds the .class file with that name (an add-on class loader might, for example, look for the bytecodes in a database instead). As the bytes for the class are loaded, they are verified to ensure that they have not been corrupted and that they do not comprise bad Java code (this is one of the lines of defense for security in Java). Once the Class object for that type is in memory, it is used to create all objects of that type. Here’s a program to prove it:
```java
//: typeinfo/SweetShop.java
// Examination of the way the class loader works.
import static net.mindview.util.Print.*;
class Candy {
static { print("Loading Candy"); }
}
```

<!--p418-->
Type Information
```java
class Gum {
static { print("Loading Gum"); }
}
class Cookie {
static { print("Loading Cookie"); }
}
public class SweetShop {
public static void main(String[] args) {
print("inside main");
new Candy();
print("After creating Candy");
try {
Class.forName("Gum");
} catch(ClassNotFoundException e) {
print("Couldn’t find Gum");
}
print("After Class.forName(\"Gum\")");
new Cookie();
print("After creating Cookie");
}
} /* Output:
inside main
Loading Candy
After creating Candy
Loading Gum
After Class.forName("Gum")
Loading Cookie
After creating Cookie
*///:~
```
Each of the classes Candy, Gum, and Cookie has a static clause that is executed as the class is loaded for the first time. Information will be printed to tell you when loading occurs for that class. In main( ), the object creations are spread out between print statements to help detect the time of loading. You can see from the output that each Class object is loaded only when it’s needed, and the static initialization is performed upon class loading. A particularly interesting line is:
```java
Class.forName("Gum");
```

<!--p419-->
All Class objects belong to the class Class. A Class object is like any other object, so you can get and manipulate a reference to it (that’s what the loader does). One of the ways to get a reference to the Class object is the static forName( ) method, which takes a String containing the textual name (watch the spelling and capitalization!) of the particular class you want a reference for. It returns a Class reference, which is being ignored here; the call to forName( ) is being made for its side effect, which is to load the class Gum if it isn’t already loaded. In the process of loading, Gum’s static clause is executed. In the preceding example, if Class.forName( ) fails because it can’t find the class you’re trying to load, it will throw a ClassNotFoundException. Here, we simply report the problem and move on, but in more sophisticated programs, you might try to fix the problem inside the exception handler. Anytime you want to use type information at run time, you must first get a reference to the appropriate Class object. Class.forName( ) is one convenient way to do this, because you don’t need an object of that type in order to get the Class reference. However, if you already have an object of the type you’re interested in, you can fetch the Class reference by calling a method that’s part of the Object root class: getClass( ). This returns the Class reference representing the actual type of the object. Class has many interesting methods; here are a few of them:
```java
//: typeinfo/toys/ToyTest.java
// Testing class Class.
package typeinfo.toys;
import static net.mindview.util.Print.*;
interface HasBatteries {}
interface Waterproof {}
interface Shoots {}
class Toy {
// Comment out the following default constructor
// to see NoSuchMethodError from (*1*)
Toy() {}
Toy(int i) {}
}
class FancyToy extends Toy
implements HasBatteries, Waterproof, Shoots {
FancyToy() { super(1); }
}
public class ToyTest {
static void printInfo(Class cc) {
print("Class name: " + cc.getName() +
" is interface? [" + cc.isInterface() + "]");
print("Simple name: " + cc.getSimpleName());
print("Canonical name : " + cc.getCanonicalName());
}
public static void main(String[] args) {
Class c = null;
try {
c = Class.forName("typeinfo.toys.FancyToy");
} catch(ClassNotFoundException e) {
print("Can’t find FancyToy");
System.exit(1);
}
printInfo(c);
for(Class face : c.getInterfaces())
printInfo(face);
Class up = c.getSuperclass();
Object obj = null;
try {
// Requires default constructor:
obj = up.newInstance();
} catch(InstantiationException e) {
print("Cannot instantiate");
System.exit(1);
} catch(IllegalAccessException e) {
print("Cannot access");
System.exit(1);
}
printInfo(obj.getClass());
}
} /* Output:
```

<!--p420-->
Type Information
```java
Class name: typeinfo.toys.FancyToy is interface? [false]
Simple name: FancyToy
Canonical name : typeinfo.toys.FancyToy
Class name: typeinfo.toys.HasBatteries is interface? [true]
Simple name: HasBatteries
Canonical name : typeinfo.toys.HasBatteries
Class name: typeinfo.toys.Waterproof is interface? [true]
Simple name: Waterproof
Canonical name : typeinfo.toys.Waterproof
Class name: typeinfo.toys.Shoots is interface? [true]
Simple name: Shoots
Canonical name : typeinfo.toys.Shoots
Class name: typeinfo.toys.Toy is interface? [false]
Simple name: Toy
Canonical name : typeinfo.toys.Toy
*///:~
```

<!--p421-->
FancyToy inherits from Toy and implements the interfaces HasBatteries, Waterproof, and Shoots. In main( ), a Class reference is created and initialized to the FancyToy Class using forName( ) inside an appropriate try block. Notice that you must use the fully qualified name (including the package name) in the string that you pass to forName( ). printInfo( ) uses getName( ) to produce the fully qualified class name, and getSimpleName( ) and getCanonicalName( ) (introduced in Java SE5) to produce the name without the package, and the fully qualified name, respectively. As its name implies, islnterface( ) tells you whether this Class object represents an interface. Thus, with the Class object you can find out just about everything you want to know about a type. The Class.getlnterfaces( ) method called in main( ) returns an array of Class objects representing the interfaces that are contained in the Class object of interest. If you have a Class object, you can also ask it for its direct base class using getSuperclass( ). This returns a Class reference that you can further query. Thus you can discover an object’s entire class hierarchy at run time. The newlnstance( ) method of Class is a way to implement a "virtual constructor," which allows you to say, "I don’t know exactly what type you are, but create yourself properly anyway." In the preceding example, up is just a Class reference with no further type information known at compile time. And when you create a new instance, you get back an Object reference. But that reference is pointing to a Toy object. Of course, before you can send any messages other than those accepted by Object, you must investigate it a bit and do some casting. In addition, the class that’s being created with newlnstance( ) must have a default constructor. Later in this chapter, you’ll see how to dynamically create objects of classes using any constructor, with the Java reflection API. Exercise 1:(1) In ToyTest.java, comment out Toy’s default constructor and explain what happens. Exercise 2:(2) Incorporate a new kind of interface into ToyTest.java and verify that it is detected and displayed properly. Exercise 3: (2) Add Rhomboid to Shapes.java. Create a Rhomboid, upcast it to a Shape, then downcast it back to a Rhomboid. Try downcasting to a Circle and see what happens. Exercise 4:(2) Modify the previous exercise so that it uses instanceof to check the type before performing the downcast. Exercise 5:(3) Implement a rotate(Shape) method in Shapes.java, such that it checks to see if it is rotating a Circle (and, if so, doesn’t perform the operation). Exercise 6:(4) Modify Shapes.java so that it can "highlight" (set a flag in) all shapes of a particular type. The toString( ) method for each derived Shape should indicate whether that Shape is "highlighted." Exercise 7:(3) Modify SweetShop.java so that each type of object creation is controlled by a command-line argument. That is, if your command line is "Java Sweetshop Candy," then only the Candy object is created. Notice how you can control which Class objects are loaded via the commandline argument. Exercise 8:(5) Write a method that takes an object and recursively prints all the classes in that object’s hierarchy. Exercise 9:(5) Modify the previous exercise so that it uses Class.getDeclaredFields( ) to also display information about the fields in a class. Exercise 10: (3) Write a program to determine whether an array of char is a primitive type or a true Object. Class literals Java provides a second way to produce the reference to the Class object: the class literal. In the preceding program this would look like:
```java
FancyToy.class;
```

<!--p422-->
which is not only simpler, but also safer since it’s checked at compile time (and thus does not need to be placed in a try block). Because it eliminates the forName( ) method call, it’s also more efficient. Class literals work with regular classes as well as interfaces, arrays, and primitive types. In addition, there’s a standard field called TYPE that exists for each of the primitive wrapper classes. The TYPE field produces a reference to the Class object for the associated primitive type, such that: ... is equivalent to ... boolean.class Boolean.TYPE char.class Character.TYPE byte.class Byte.TYPE short.class Short.TYPE int.class Integer.TYPE long.class Long.TYPE float.class Float.TYPE double.class Double.TYPE void.class Void.TYPE My preference is to use the ".class" versions if you can, since they’re more consistent with regular classes. Type Information It’s interesting to note that creating a reference to a Class object using ".class" doesn’t automatically initialize the Class object. There are actually three steps in preparing a class for use: 1.Loading, which is performed by the class loader. This finds the bytecodes (usually, but not necessarily, on your disk in your classpath) and creates a Class object from those bytecodes. 2.Linking. The link phase verifies the bytecodes in the class, allocates storage for static fields, and if necessary, resolves all references to other classes made by this class. 3.Initialization. If there’s a superclass, initialize that. Execute static initializers and static initialization blocks. Initialization is delayed until the first reference to a static method (the constructor is implicitly static) or to a non-constant static field:

<!--p423-->
```java
//: typeinfo/ClassInitialization.java
import java.util.*;
class Initable {
static final int staticFinal = 47;
static final int staticFinal2 =
ClassInitialization.rand.nextInt(1000);
static {
System.out.println("Initializing Initable");
}
}
class Initable2 {
static int staticNonFinal = 147;
static {
System.out.println("Initializing Initable2");
}
}
class Initable3 {
static int staticNonFinal = 74;
static {
System.out.println("Initializing Initable3");
}
}
public class ClassInitialization {
public static Random rand = new Random(47);
public static void main(String[] args) throws Exception {
Class initable = Initable.class;
System.out.println("After creating Initable ref");
// Does not trigger initialization:
System.out.println(Initable.staticFinal);
// Does trigger initialization:
System.out.println(Initable.staticFinal2);
// Does trigger initialization:
System.out.println(Initable2.staticNonFinal);
Class initable3 = Class.forName("Initable3");
System.out.println("After creating Initable3 ref");
System.out.println(Initable3.staticNonFinal);
}
} /* Output:
After creating Initable ref
Initializing Initable
Initializing Initable2
Initializing Initable3
After creating Initable3 ref
*///:~
```
Effectively, initialization is "as lazy as possible." From the creation of the initable reference, you can see that just using the .class syntax to get a reference to the class doesn’t cause initialization. However, Class.forName( ) initializes the class immediately in order to produce the Class reference, as you can see in the creation of initable3. If a static final value is a "compile-time constant," such as Initable.staticFinal, that value can be read without causing the Initable class to be initialized. Making a field static and final, however, does not guarantee this behavior: accessing Initable.staticFinal2 forces class initialization because it cannot be a compile-time constant. If a static field is not final, accessing it always requires linking (to allocate storage for the field) and initialization (to initialize that storage) before it can be read, as you can see in the access to Initable2.staticNonFinal. Generic class references A Class reference points to a Class object, which manufactures instances of classes and contains all the method code for those instances. It also contains the statics for that class. So a Class reference really does indicate the exact type of what it’s pointing to: an object of the class Class. However, the designers of Java SE5 saw an opportunity to make this a bit more specific by allowing you to constrain the type of Class object that the Class reference is pointing to, using the generic syntax. In the following example, both syntaxes are correct:
```java
//: typeinfo/GenericClassReferences.java
public class GenericClassReferences {
public static void main(String[] args) {
Class intClass = int.class;
Class<Integer> genericIntClass = int.class;
genericIntClass = Integer.class; // Same thing
intClass = double.class;
// genericIntClass = double.class; // Illegal
}
} ///:~
```
The ordinary class reference does not produce a warning. However, you can see that the ordinary class reference can be reassigned to any other Class object, whereas the generic class reference can only be assigned to its declared type. By using the generic syntax, you allow the compiler to enforce extra type checking. What if you’d like to loosen the constraint a little? Initially, it seems like you ought to be able to do something like:
```java
Class<Number> genericNumberClass = int.class;
```

<!--p424-->
This would seem to make sense because Integer is inherited from Number. But this doesn’t work, because the Integer Class object is not a subclass of the Number Class Type Information object (this may seem like a subtle distinction; we’ll look into it more deeply in the Generics chapter). To loosen the constraints when using generic Class references, I employ the wildcard, which is part of Java generics. The wildcard symbol is ‘?’, and it indicates "anything." So we can add wildcards to the ordinary Class reference in the above example and produce the same results:
```java
//: typeinfo/WildcardClassReferences.java
public class WildcardClassReferences {
public static void main(String[] args) {
Class<?> intClass = int.class;
intClass = double.class;
}
} ///:~
```
In Java SE5, Class<?> is preferred over plain Class, even though they are equivalent and the plain Class, as you saw, doesn’t produce a compiler warning. The benefit of Class<?> is that it indicates that you aren’t just using a non-specific class reference by accident, or out of ignorance. You chose the non-specific version. In order to create a Class reference that is constrained to a type or any subtype, you combine the wildcard with the extends keyword to create a bound. So instead of just saying Class<Number>, you say:
```java
//: typeinfo/BoundedClassReferences.java
public class BoundedClassReferences {
public static void main(String[] args) {
Class<? extends Number> bounded = int.class;
bounded = double.class;
bounded = Number.class;
// Or anything else derived from Number.
}
} ///:~
```
The reason for adding the generic syntax to Class references is only to provide compile-time type checking, so that if you do something wrong you find out about it a little sooner. You can’t actually go astray with ordinary Class references, but if you make a mistake you won’t find out until run time, which can be inconvenient. Here’s an example that uses the generic class syntax. It stores a class reference, and later produces a List filled with objects that it generates using newlnstance( ):

<!--p425-->
```java
//: typeinfo/FilledList.java
import java.util.*;
class CountedInteger {
private static long counter;
private final long id = counter++;
public String toString() { return Long.toString(id); }
}
public class FilledList<T> {
private Class<T> type;
public FilledList(Class<T> type) { this.type = type; }
public List<T> create(int nElements) {
List<T> result = new ArrayList<T>();
try {
for(int i = 0; i < nElements; i++)
result.add(type.newInstance());
} catch(Exception e) {
throw new RuntimeException(e);
}
return result;
}
public static void main(String[] args) {
FilledList<CountedInteger> fl =
new FilledList<CountedInteger>(CountedInteger.class);
System.out.println(fl.create(15));
}
} /* Output:
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
*///:~
```
Notice that this class must assume that any type that it works with has a default constructor (one without arguments), and you’ll get an exception if that isn’t the case. The compiler does not issue any warnings for this program. An interesting thing happens when you use the generic syntax for Class objects: newlnstance( ) will return the exact type of the object, rather than just a basic Object as you saw in ToyTest.java. This is somewhat limited:
```java
//: typeinfo/toys/GenericToyTest.java
// Testing class Class.
package typeinfo.toys;
public class GenericToyTest {
public static void main(String[] args) throws Exception {
Class<FancyToy> ftClass = FancyToy.class;
// Produces exact type:
FancyToy fancyToy = ftClass.newInstance();
Class<? super FancyToy> up = ftClass.getSuperclass();
// This won’t compile:
// Class<Toy> up2 = ftClass.getSuperclass();
// Only produces Object:
Object obj = up.newInstance();
}
} ///:~
```
If you get the superclass, the compiler will only allow you to say that the superclass reference is "some class that is a superclass of FancyToy"as seen in the expression Class <? super FancyToy >. It will not accept a declaration of Class<Toy>. This seems a bit strange because getSuperclass( ) returns the base class (not interface) and the compiler knows what that class is at compile time—in this case, Toy.class, not just "some superclass of FancyToy." In any event, because of the vagueness, the return value of up.newlnstance( ) is not a precise type, but just an Object. New cast syntax Java SE5 also adds a casting syntax for use with Class references, which is the cast( ) method:
```java
//: typeinfo/ClassCasts.java
class Building {}
class House extends Building {}
```

<!--p426-->
Type Information
```java
public class ClassCasts {
public static void main(String[] args) {
Building b = new House();
Class<House> houseType = House.class;
House h = houseType.cast(b);
h = (House)b; // ... or just do this.
}
} ///:~
```
The cast( ) method takes the argument object and casts it to the type of the Class reference. Of course, if you look at the above code it seems like a lot of extra work compared to the last line in main( ), which does the same thing. The new casting syntax is useful for situations where you can’t just use an ordinary cast. This usually happens when you’re writing generic code (which you’ll learn about in the Generics chapter), and you’ve stored a Class reference that you want to use to cast with at a later time. It turns out to be a rare thing—I found only one instance where cast( ) was used in the entire Java SE5 library (it was in com.sun.mirror.util.DeclarationFilter). Another new feature had no usage in the Java SE5 library: Class.asSubclass( ). This allows you to cast the class object to a more specific type. Checking before a cast So far, you’ve seen forms of RTTI, including: 1.The classic cast; e.g., "(Shape)," which uses RTTI to make sure the cast is correct. This will throw a ClassCastException if you’ve performed a bad cast. 2.The Class object representing the type of your object. The Class object can be queried for useful runtime information. In C++, the classic cast "(Shape)"does not perform RTTI. It simply tells the compiler to treat the object as the new type. In Java, which does perform the type check, this cast is often called a "type-safe downcast." The reason for the term "downcast" is the historical arrangement of the class hierarchy diagram. If casting a Circle to a Shape is an upcast, then casting a Shape to a Circle is a downcast. However, because it knows that a Circle is also a Shape, the compiler freely allows an upcast assignment, without requiring any explicit cast syntax. The compiler cannot know, given a Shape, what that Shape actually is—it could be exactly a Shape, or it could be a subtype of Shape, such as a Circle, Square, Triangle or some other type. At compile time, the compiler only sees a Shape. Thus, it won’t allow you to perform a downcast assignment without using an explicit cast, to tell it that you have extra information that allows you to know that it is a particular type (the compiler will check to see if that downcast is reasonable, so it won’t let you downcast to a type that’s not actually a subclass). There’s a third form of RTTI in Java. This is the keyword instanceof, which tells you if an object is an instance of a particular type. It returns a boolean so you use it in the form of a question, like this:
```java
if(x instanceof Dog)
((Dog)x).bark();
```

<!--p427-->
The if statement checks to see if the object x belongs to the class Dog before casting x to a Dog. It’s important to use instanceof before a downcast when you don’t have other information that tells you the type of the object; otherwise, you’ll end up with a ClassCastException. Ordinarily, you might be hunting for one type (triangles to turn purple, for example), but you can easily tally all of the objects by using instanceof. For example, suppose you have a family of classes to describe Pets (and their people, a feature which will come in handy in a later example). Each Individual in the hierarchy has an id and an optional name. Although the classes that follow inherit from Individual, there are some complexities in the Individual class, so that code will be shown and explained in the Containers in Depth chapter. As you can see, it’s not really necessary to see the code for Individual at this point—you only need to know that you can create it with or without a name, and that each Individual has a method id( ) that returns a unique identifier (created by counting each object). There’s also a toString( ) method; if you don’t provide a name for an Individual, toString( ) only produces the simple type name. Here is the class hierarchy that inherits from Individual:
```java
//: typeinfo/pets/Person.java
package typeinfo.pets;
public class Person extends Individual {
public Person(String name) { super(name); }
} ///:~
//: typeinfo/pets/Pet.java
package typeinfo.pets;
public class Pet extends Individual {
public Pet(String name) { super(name); }
public Pet() { super(); }
} ///:~
//: typeinfo/pets/Dog.java
package typeinfo.pets;
public class Dog extends Pet {
public Dog(String name) { super(name); }
public Dog() { super(); }
} ///:~
//: typeinfo/pets/Mutt.java
package typeinfo.pets;
public class Mutt extends Dog {
public Mutt(String name) { super(name); }
public Mutt() { super(); }
} ///:~
//: typeinfo/pets/Pug.java
package typeinfo.pets;
public class Pug extends Dog {
public Pug(String name) { super(name); }
public Pug() { super(); }
} ///:~
//: typeinfo/pets/Cat.java
package typeinfo.pets;
public class Cat extends Pet {
public Cat(String name) { super(name); }
public Cat() { super(); }
} ///:~
//: typeinfo/pets/EgyptianMau.java
```

<!--p428-->
Type Information
```java
package typeinfo.pets;
public class EgyptianMau extends Cat {
public EgyptianMau(String name) { super(name); }
public EgyptianMau() { super(); }
} ///:~
//: typeinfo/pets/Manx.java
package typeinfo.pets;
public class Manx extends Cat {
public Manx(String name) { super(name); }
public Manx() { super(); }
} ///:~
//: typeinfo/pets/Cymric.java
package typeinfo.pets;
public class Cymric extends Manx {
public Cymric(String name) { super(name); }
public Cymric() { super(); }
} ///:~
//: typeinfo/pets/Rodent.java
package typeinfo.pets;
public class Rodent extends Pet {
public Rodent(String name) { super(name); }
public Rodent() { super(); }
} ///:~
//: typeinfo/pets/Rat.java
package typeinfo.pets;
public class Rat extends Rodent {
public Rat(String name) { super(name); }
public Rat() { super(); }
} ///:~
//: typeinfo/pets/Mouse.java
package typeinfo.pets;
public class Mouse extends Rodent {
public Mouse(String name) { super(name); }
public Mouse() { super(); }
} ///:~
//: typeinfo/pets/Hamster.java
package typeinfo.pets;
public class Hamster extends Rodent {
public Hamster(String name) { super(name); }
public Hamster() { super(); }
} ///:~
```
Next, we need a way to randomly create different types of pets, and for convenience, to create arrays and Lists of pets. To allow this tool to evolve through several different implementations, we’ll define it as an abstract class:

<!--p429-->
```java
//: typeinfo/pets/PetCreator.java
// Creates random sequences of Pets.
package typeinfo.pets;
import java.util.*;
public abstract class PetCreator {
private Random rand = new Random(47);
// The List of the different types of Pet to create:
public abstract List<Class<? extends Pet>> types();
public Pet randomPet() { // Create one random Pet
int n = rand.nextInt(types().size());
try {
return types().get(n).newInstance();
} catch(InstantiationException e) {
throw new RuntimeException(e);
} catch(IllegalAccessException e) {
throw new RuntimeException(e);
}
}
public Pet[] createArray(int size) {
Pet[] result = new Pet[size];
for(int i = 0; i < size; i++)
result[i] = randomPet();
return result;
}
public ArrayList<Pet> arrayList(int size) {
ArrayList<Pet> result = new ArrayList<Pet>();
Collections.addAll(result, createArray(size));
return result;
}
} ///:~
```
The abstract getTypes( ) method defers to a derived class to get the List of Class objects (this is a variation of the Template Method design pattern). Notice that the type of class is specified to be "anything derived from Pet,"so that newlnstance( ) produces a Pet without requiring a cast. randomPet( ) randomly indexes into the List and uses the selected Class object to generate a new instance of that class with Class.newlnstance( ). The createArray( ) method uses randomPet( ) to fill an array, and arrayList( ) uses createArray( ) in turn. You can get two kinds of exceptions when calling newlnstance( ). You can see these handled in the catch clauses following the try block. Again, the names of the exceptions are relatively useful explanations of what went wrong (IllegalAccessException relates to a violation of the Java security mechanism, in this case if the default constructor is private). When you derive a subclass of PetCreator, the only thing you need to supply is the List of the types of pet that you want to create using randomPet( ) and the other methods. The getTypes( ) method will normally just return a reference to a static List. Here’s an implementation using forName( ):
```java
//: typeinfo/pets/ForNameCreator.java
package typeinfo.pets;
import java.util.*;
public class ForNameCreator extends PetCreator {
private static List<Class<? extends Pet>> types =
new ArrayList<Class<? extends Pet>>();
// Types that you want to be randomly created:
private static String[] typeNames = {
"typeinfo.pets.Mutt",
"typeinfo.pets.Pug",
"typeinfo.pets.EgyptianMau",
"typeinfo.pets.Manx",
"typeinfo.pets.Cymric",
```

<!--p430-->
Type Information
```java
"typeinfo.pets.Rat",
"typeinfo.pets.Mouse",
"typeinfo.pets.Hamster"
};
@SuppressWarnings("unchecked")
private static void loader() {
try {
for(String name : typeNames)
types.add(
(Class<? extends Pet>)Class.forName(name));
} catch(ClassNotFoundException e) {
throw new RuntimeException(e);
}
}
static { loader(); }
public List<Class<? extends Pet>> types() {return types;}
} ///:~
```
The loader( ) method creates the List of Class objects using Class.forName( ). This may generate a ClassNotFoundException, which makes sense since you’re passing it a String which cannot be validated at compile time. Since the Pet objects are in package typeinfo, the package name must be used when referring to the classes. In order to produce a typed List of Class objects, a cast is required, which produces a compile-time warning. The loader( ) method is defined separately and then placed inside a static initialization clause because the @SuppressWarnings annotation cannot be placed directly onto the static initialization clause. To count Pets, we need a tool that keeps track of the quantities of various different types of Pets. A Map is perfect for this; the keys are the Pet type names and the values are Integers to hold the Pet quantities. This way, you can say, "How many Hamster objects are there?" We can use instanceof to count Pets:

<!--p431-->
```java
//: typeinfo/PetCount.java
// Using instanceof.
import typeinfo.pets.*;
import java.util.*;
import static net.mindview.util.Print.*;
public class PetCount {
static class PetCounter extends HashMap<String,Integer> {
public void count(String type) {
Integer quantity = get(type);
if(quantity == null)
put(type, 1);
else
put(type, quantity + 1);
}
}
public static void
countPets(PetCreator creator) {
PetCounter counter= new PetCounter();
for(Pet pet : creator.createArray(20)) {
// List each individual pet:
printnb(pet.getClass().getSimpleName() + " ");
if(pet instanceof Pet)
counter.count("Pet");
if(pet instanceof Dog)
counter.count("Dog");
if(pet instanceof Mutt)
counter.count("Mutt");
if(pet instanceof Pug)
counter.count("Pug");
if(pet instanceof Cat)
counter.count("Cat");
if(pet instanceof Manx)
counter.count("EgyptianMau");
if(pet instanceof Manx)
counter.count("Manx");
if(pet instanceof Manx)
counter.count("Cymric");
if(pet instanceof Rodent)
counter.count("Rodent");
if(pet instanceof Rat)
counter.count("Rat");
if(pet instanceof Mouse)
counter.count("Mouse");
if(pet instanceof Hamster)
counter.count("Hamster");
}
// Show the counts:
print();
print(counter);
}
public static void main(String[] args) {
countPets(new ForNameCreator());
}
} /* Output:
Rat Manx Cymric Mutt Pug Cymric Pug Manx Cymric Rat EgyptianMau Hamster
EgyptianMau Mutt Mutt Cymric Mouse Pug Mouse Cymric
{Pug=3, Cat=9, Hamster=1, Cymric=7, Mouse=2, Mutt=3, Rodent=5, Pet=20,
Manx=7, EgyptianMau=7, Dog=6, Rat=2}
*///:~
```
In countPets( ), an array is randomly filled with Pets using a PetCreator. Then each Pet in the array is tested and counted using instanceof. There’s a rather narrow restriction on instanceof: You can compare it to a named type only, and not to a Class object. In the preceding example you might feel that it’s tedious to write out all of those instanceof expressions, and you’re right. But there is no way to cleverly automate instanceof by creating an array of Class objects and comparing it to those instead (stay tuned—you’ll see an alternative). This isn’t as great a restriction as you might think, because you’ll eventually understand that your design is probably flawed if you end up writing a lot of instanceof expressions. Using class literals If we reimplement the PetCreator using class literals, the result is cleaner in many ways:
```java
//: typeinfo/pets/LiteralPetCreator.java
// Using class literals.
package typeinfo.pets;
import java.util.*;
public class LiteralPetCreator extends PetCreator {
// No try block needed.
@SuppressWarnings("unchecked")
public static final List<Class<? extends Pet>> allTypes =
Collections.unmodifiableList(Arrays.asList(
Pet.class, Dog.class, Cat.class, Rodent.class,
Mutt.class, Pug.class, EgyptianMau.class, Manx.class,
Cymric.class, Rat.class, Mouse.class,Hamster.class));
// Types for random creation:
private static final List<Class<? extends Pet>> types =
allTypes.subList(allTypes.indexOf(Mutt.class),
```

<!--p432-->
Type Information
```java
allTypes.size());
public List<Class<? extends Pet>> types() {
return types;
}
public static void main(String[] args) {
System.out.println(types);
}
} /* Output:
[class typeinfo.pets.Mutt, class typeinfo.pets.Pug, class
typeinfo.pets.EgyptianMau, class typeinfo.pets.Manx, class
typeinfo.pets.Cymric, class typeinfo.pets.Rat, class
typeinfo.pets.Mouse, class typeinfo.pets.Hamster]
*///:~
```
In the upcoming PetCount3.java example, we need to pre-load a Map with all the Pet types (not just the ones that are to be randomly generated), so the allTypes List is necessary. The types list is the portion of allTypes (created using List.subList( )) that includes the exact pet types, so it is used for random Pet generation. This time, the creation of types does not need to be surrounded by a try block since it’s evaluated at compile time and thus won’t throw any exceptions, unlike Class.forName( ). We now have two implementations of PetCreator in the typeinfo.pets library. In order to provide the second one as a default implementation, we can create a Faqade that utilizes LiteralPetCreator:
```java
//: typeinfo/pets/Pets.java
// Facade to produce a default PetCreator.
package typeinfo.pets;
import java.util.*;
public class Pets {
public static final PetCreator creator =
new LiteralPetCreator();
public static Pet randomPet() {
return creator.randomPet();
}
public static Pet[] createArray(int size) {
return creator.createArray(size);
}
public static ArrayList<Pet> arrayList(int size) {
return creator.arrayList(size);
}
} ///:~
```
This also provides indirection to randomPet( ), createArray( ) and arrayList( ). Because PetCount.countPets( ) takes a PetCreator argument, we can easily test the LiteralPetCreator (via the above Facade):
```java
//: typeinfo/PetCount2.java
import typeinfo.pets.*;
public class PetCount2 {
public static void main(String[] args) {
PetCount.countPets(Pets.creator);
}
} /* (Execute to see output) *///:~
```

<!--p433-->
The output is the same as that of PetCount.java.
## A dynamic instanceof
The Class.islnstance( ) method provides a way to dynamically test the type of an object. Thus, all those tedious instanceof statements can be removed from PetCount.java:
```java
//: typeinfo/PetCount3.java
// Using isInstance()
import typeinfo.pets.*;
import java.util.*;
import net.mindview.util.*;
import static net.mindview.util.Print.*;
public class PetCount3 {
static class PetCounter
extends LinkedHashMap<Class<? extends Pet>,Integer> {
public PetCounter() {
super(MapData.map(LiteralPetCreator.allTypes, 0));
}
public void count(Pet pet) {
// Class.isInstance() eliminates instanceofs:
for(Map.Entry<Class<? extends Pet>,Integer> pair
: entrySet())
if(pair.getKey().isInstance(pet))
put(pair.getKey(), pair.getValue() + 1);
}
public String toString() {
StringBuilder result = new StringBuilder("{");
for(Map.Entry<Class<? extends Pet>,Integer> pair
: entrySet()) {
result.append(pair.getKey().getSimpleName());
result.append("=");
result.append(pair.getValue());
result.append(", ");
}
result.delete(result.length()-2, result.length());
result.append("}");
return result.toString();
}
}
public static void main(String[] args) {
PetCounter petCount = new PetCounter();
for(Pet pet : Pets.createArray(20)) {
printnb(pet.getClass().getSimpleName() + " ");
petCount.count(pet);
}
print();
print(petCount);
}
} /* Output:
Rat Manx Cymric Mutt Pug Cymric Pug Manx Cymric Rat EgyptianMau Hamster
EgyptianMau Mutt Mutt Cymric Mouse Pug Mouse Cymric
{Pet=20, Dog=6, Cat=9, Rodent=5, Mutt=3, Pug=3, EgyptianMau=2, Manx=7,
Cymric=5, Rat=2, Mouse=2, Hamster=1}
*///:~
```

<!--p434-->
In order to count all the different types of Pet, the PetCounter Map is preloaded with the types from LiteralPetCreator.allTypes. This uses the net.mindview.util.MapData class, which takes an Iterable (the allTypes List) and a constant value (zero, in this case), and fills the Map with keys taken from allTypes and values of zero). Without pre-loading the Map, you would only end up counting the types that are randomly generated, and not the base types like Pet and Cat. Type Information You can see that the isInstance( ) method has eliminated the need for the instanceof expressions. In addition, this means that you can add new types of Pet simply by changing the LiteralPetCreator.types array; the rest of the program does not need modification (as it did when using the instanceof expressions). The toString( ) method has been overloaded for easier-to-read output that still matches the typical output that you see when printing a Map. Counting recursively The Map in PetCount3.PetCounter was pre-loaded with all the different Pet classes. Instead of pre-loading the map, we can use Class.isAssignableFrom( ) and create a general-purpose tool that is not limited to counting Pets:
```java
//: net/mindview/util/TypeCounter.java
// Counts instances of a type family.
package net.mindview.util;
import java.util.*;
public class TypeCounter extends HashMap<Class<?>,Integer>{
private Class<?> baseType;
public TypeCounter(Class<?> baseType) {
this.baseType = baseType;
}
public void count(Object obj) {
Class<?> type = obj.getClass();
if(!baseType.isAssignableFrom(type))
throw new RuntimeException(obj + " incorrect type: "
+ type + ", should be type or subtype of "
+ baseType);
countClass(type);
}
private void countClass(Class<?> type) {
Integer quantity = get(type);
put(type, quantity == null ? 1 : quantity + 1);
Class<?> superClass = type.getSuperclass();
if(superClass != null &&
baseType.isAssignableFrom(superClass))
countClass(superClass);
}
public String toString() {
StringBuilder result = new StringBuilder("{");
for(Map.Entry<Class<?>,Integer> pair : entrySet()) {
result.append(pair.getKey().getSimpleName());
result.append("=");
result.append(pair.getValue());
result.append(", ");
}
result.delete(result.length()-2, result.length());
result.append("}");
return result.toString();
}
} ///:~
```

<!--p435-->
The count( ) method gets the Class of its argument, and uses isAssignableFrom( ) to perform a runtime check to verify that the object that you’ve passed actually belongs to the hierarchy of interest. countClass( ) first counts the exact type of the class. Then, if baseType is assignable from the superclass, countClass( ) is called recursively on the superclass.
```java
//: typeinfo/PetCount4.java
import typeinfo.pets.*;
import net.mindview.util.*;
import static net.mindview.util.Print.*;
public class PetCount4 {
public static void main(String[] args) {
TypeCounter counter = new TypeCounter(Pet.class);
for(Pet pet : Pets.createArray(20)) {
printnb(pet.getClass().getSimpleName() + " ");
counter.count(pet);
}
print();
print(counter);
}
} /* Output: (Sample)
Rat Manx Cymric Mutt Pug Cymric Pug Manx Cymric Rat EgyptianMau Hamster
EgyptianMau Mutt Mutt Cymric Mouse Pug Mouse Cymric
{Mouse=2, Dog=6, Manx=7, EgyptianMau=2, Rodent=5, Pug=3, Mutt=3,
Cymric=5, Cat=9, Hamster=1, Pet=20, Rat=2}
*///:~
```

<!--p436-->
As you can see from the output, both base types as well as exact types are counted. Exercise 11:(2) Add Gerbil to the typeinfo.pets library and modify all the examples in this chapter to adapt to this new class. Exercise 12: (3) Use TypeCounter with the CoffeeGenerator.java class in the Generics chapter. Exercise 13:(3) Use TypeCounter with the RegisteredFactories.java example in this chapter. Registered factories A problem with generating objects of the Pets hierarchy is the fact that every time you add a new type of Pet to the hierarchy you must remember to add it to the entries in LiteralPetCreator.java. In a system where you add more classes on a regular basis this can become problematic. You might think of adding a static initializer to each subclass, so that the initializer would add its class to a list somewhere. Unfortunately, static initializers are only called when the class is first loaded, so you have a chicken-and-egg problem: The generator doesn’t have the class in its list, so it can never create an object of that class, so the class won’t get loaded and placed in the list. Basically, you’re forced to create the list yourself, by hand (unless you want to write a tool that searches through and analyzes your source code, then creates and compiles the list). So the best you can probably do is to put the list in one central, obvious place. The base class for the hierarchy of interest is probably the best place. The other change we’ll make here is to defer the creation of the object to the class itself, using the Factory Method design pattern. A factory method can be called polymorphically, and creates an object of the appropriate type for you. In this very simple version, the factory method is the create( ) method in the Factory interface: Type Information
```java
//: typeinfo/factory/Factory.java
package typeinfo.factory;
public interface Factory<T> { T create(); } ///:~
```
The generic parameter T allows create( ) to return a different type for each implementation of Factory. This also makes use of covariant return types. In this example, the base class Part contains a List of factory objects. Factories for types that should be produced by the createRandom( ) method are "registered" with the base class by adding them to the partFactories List:

<!--p437-->
```java
//: typeinfo/RegisteredFactories.java
// Registering Class Factories in the base class.
import typeinfo.factory.*;
import java.util.*;
class Part {
public String toString() {
return getClass().getSimpleName();
}
static List<Factory<? extends Part>> partFactories =
new ArrayList<Factory<? extends Part>>();
static {
// Collections.addAll() gives an "unchecked generic
// array creation ... for varargs parameter" warning.
partFactories.add(new FuelFilter.Factory());
partFactories.add(new AirFilter.Factory());
partFactories.add(new CabinAirFilter.Factory());
partFactories.add(new OilFilter.Factory());
partFactories.add(new FanBelt.Factory());
partFactories.add(new PowerSteeringBelt.Factory());
partFactories.add(new GeneratorBelt.Factory());
}
private static Random rand = new Random(47);
public static Part createRandom() {
int n = rand.nextInt(partFactories.size());
return partFactories.get(n).create();
}
}
class Filter extends Part {}
class FuelFilter extends Filter {
// Create a Class Factory for each specific type:
public static class Factory
implements typeinfo.factory.Factory<FuelFilter> {
public FuelFilter create() { return new FuelFilter(); }
}
}
class AirFilter extends Filter {
public static class Factory
implements typeinfo.factory.Factory<AirFilter> {
public AirFilter create() { return new AirFilter(); }
}
}
class CabinAirFilter extends Filter {
public static class Factory
implements typeinfo.factory.Factory<CabinAirFilter> {
public CabinAirFilter create() {
return new CabinAirFilter();
}
}
}
class OilFilter extends Filter {
public static class Factory
implements typeinfo.factory.Factory<OilFilter> {
public OilFilter create() { return new OilFilter(); }
}
}
class Belt extends Part {}
class FanBelt extends Belt {
public static class Factory
implements typeinfo.factory.Factory<FanBelt> {
public FanBelt create() { return new FanBelt(); }
}
}
class GeneratorBelt extends Belt {
public static class Factory
implements typeinfo.factory.Factory<GeneratorBelt> {
public GeneratorBelt create() {
return new GeneratorBelt();
}
}
}
class PowerSteeringBelt extends Belt {
public static class Factory
implements typeinfo.factory.Factory<PowerSteeringBelt> {
public PowerSteeringBelt create() {
return new PowerSteeringBelt();
}
}
}
public class RegisteredFactories {
public static void main(String[] args) {
for(int i = 0; i < 10; i++)
System.out.println(Part.createRandom());
}
} /* Output:
GeneratorBelt
CabinAirFilter
GeneratorBelt
AirFilter
PowerSteeringBelt
CabinAirFilter
FuelFilter
PowerSteeringBelt
PowerSteeringBelt
FuelFilter
*///:~
```

<!--p438-->
Not all classes in the hierarchy should be instantiated; in this case Filter and Belt are just classifiers so you do not create an instance of either one, but only of their subclasses. If a class should be created by createRandom( ), it contains an inner Factory class. The only way to reuse the name Factory as seen above is by qualifying typeinfo.factory.Factory. Although you can use Collections.addAll( ) to add the factories to the list, the compiler expresses its unhappiness with a warning about a "generic array creation" (which is supposed Type Information to be impossible, as you’ll see in the Generics chapter), so I reverted to calling add( ). The createRandom( ) method randomly selects a factory object from partFactories and calls its create( ) to produce a new Part. Exercise 14:(4) A constructor is a kind of factory method. Modify RegisteredFactories.java so that instead of using an explicit factory, the class object is stored in the List, and newlnstance( ) is used to create each object. Exercise 15:(4) Implement a new PetCreator using Registered Factories, and modify the Pets Facade so that it uses this one instead of the other two. Ensure that the rest of the examples that use Pets .Java still work correctly. Exercise 16:(4) Modify the Coffee hierarchy in the Generics chapter to use Registered Factories.
## instanceof vs. Class equivalence
When you are querying for type information, there’s an important difference between either form of instanceof (that is, instanceof or islnstance( ), which produce equivalent results) and the direct comparison of the Class objects. Here’s an example that demonstrates the difference:

<!--p439-->
```java
//: typeinfo/FamilyVsExactType.java
// The difference between instanceof and class
package typeinfo;
import static net.mindview.util.Print.*;
class Base {}
class Derived extends Base {}
public class FamilyVsExactType {
static void test(Object x) {
print("Testing x of type " + x.getClass());
print("x instanceof Base " + (x instanceof Base));
print("x instanceof Derived "+ (x instanceof Derived));
print("Base.isInstance(x) "+ Base.class.isInstance(x));
print("Derived.isInstance(x) " +
Derived.class.isInstance(x));
print("x.getClass() == Base.class " +
(x.getClass() == Base.class));
print("x.getClass() == Derived.class " +
(x.getClass() == Derived.class));
print("x.getClass().equals(Base.class)) "+
(x.getClass().equals(Base.class)));
print("x.getClass().equals(Derived.class)) " +
(x.getClass().equals(Derived.class)));
}
public static void main(String[] args) {
test(new Base());
test(new Derived());
}
} /* Output:
Testing x of type class typeinfo.Base
x instanceof Base true
x instanceof Derived false
Base.isInstance(x) true
Derived.isInstance(x) false
x.getClass() == Base.class true
x.getClass() == Derived.class false
x.getClass().equals(Base.class)) true
x.getClass().equals(Derived.class)) false
Testing x of type class typeinfo.Derived
x instanceof Base true
x instanceof Derived true
Base.isInstance(x) true
Derived.isInstance(x) true
x.getClass() == Base.class false
x.getClass() == Derived.class true
x.getClass().equals(Base.class)) false
x.getClass().equals(Derived.class)) true
*///:~
```

<!--p440-->
The test( ) method performs type checking with its argument using both forms of instanceof. It then gets the Class reference and uses == and equals( ) to test for equality of the Class objects. Reassuringly, instanceof and islnstance( ) produce exactly the same results, as do equals( ) and ==. But the tests themselves draw different conclusions. In keeping with the concept of type, instanceof says, "Are you this class, or a class derived from this class?" On the other hand, if you compare the actual Class objects using ==, there is no concern with inheritance—it’s either the exact type or it isn’t. Reflection: runtime class information If you don’t know the precise type of an object, RTTI will tell you. However, there’s a limitation: The type must be known at compile time in order for you to detect it using RTTI and to do something useful with the information. Put another way, the compiler must know about all the classes you’re working with. This doesn’t seem like that much of a limitation at first, but suppose you’re given a reference to an object that’s not in your program space. In fact, the class of the object isn’t even available to your program at compile time. For example, suppose you get a bunch of bytes from a disk file or from a network connection, and you’re told that those bytes represent a class. Since this class shows up long after the compiler generates the code for your program, how can you possibly use such a class? In a traditional programming environment, this seems like a far-fetched scenario. But as we move into a larger programming world, there are important cases in which this happens. The first is component-based programming, in which you build projects using Rapid Application Development (RAD) in an Application Builder Integrated Development Environment, which I shall refer to simply as an IDE. This is a visual approach to creating a program by moving icons that represent components onto a form. These components are then configured by setting some of their values at program time. This design-time configuration requires that any component be instantiable, that it exposes parts of itself, and that it allows its properties to be read and modified. In addition, components that handle Graphical User Interface (GUI) events must expose information about appropriate methods so that the IDE can assist the programmer in overriding these event-handling methods. Reflection provides the mechanism to detect the available methods and produce the method names. Java provides a structure for component-based programming through JavaBeans (described in the Graphical User Interfaces chapter). Another compelling motivation for discovering class information at run time is to provide the ability to create and execute objects on remote platforms, across a network. This is called Remote Method Invocation (RMI), and it allows a Java program to have objects distributed across many machines. This distribution can happen for a number of reasons. For example, perhaps you’re doing a computation-intensive task, and in order to speed things up, you want to break it up and put pieces on machines that are idle. In other situations you might want to Type Information place code that handles particular types of tasks (e.g., "Business Rules" in a multitier client/server architecture) on a particular machine, so the machine becomes a common repository describing those actions, and it can be easily changed to affect everyone in the system. (This is an interesting development, since the machine exists solely to make software changes easy!) Along these lines, distributed computing also supports specialized hardware that might be good at a particular task—matrix inversions, for example—but inappropriate or too expensive for generalpurpose programming. The class Class supports the concept of reflection, along with the java.lang.reflect library which contains the classes Field, Method, and Constructor (each of which implements the Member interface). Objects of these types are created by the JVM at run time to represent the corresponding member in the unknown class. You can then use the Constructors to create new objects, the get( ) and set( ) methods to read and modify the fields associated with Field objects, and the invoke( ) method to call a method associated with a Method object. In addition, you can call the convenience methods getFields( ), getMethods( ), getConstructors( ), etc., to return arrays of the objects representing the fields, methods, and constructors. (You can find out more by looking up the class Class in the JDK documentation.) Thus, the class information for anonymous objects can be completely determined at run time, and nothing need be known at compile time. It’s important to realize that there’s nothing magic about reflection. When you’re using reflection to interact with an object of an unknown type, the JVM will simply look at the object and see that it belongs to a particular class (just like ordinary RTTI). Before anything can be done with it, the Class object must be loaded. Thus, the .class file for that particular type must still be available to the JVM, either on the local machine or across the network. So the true difference between RTTI and reflection is that with RTTI, the compiler opens and examines the .class file at compile time. Put another way, you can call all the methods of an object in the "normal" way. With reflection, the .class file is unavailable at compile time; it is opened and examined by the runtime environment. A class method extractor Normally you won’t need to use the reflection tools directly, but they can be helpful when you need to create more dynamic code. Reflection is in the language to support other Java features, such as object serialization and JavaBeans (both covered later in the book). However, there are times when it’s quite useful to dynamically extract information about a class. Consider a class method extractor. Looking at a class definition source code or JDK documentation shows only the methods that are defined or overridden within that class definition. But there might be dozens more available to you that have come from base classes. To locate these is both tedious and time consuming.1Fortunately, reflection provides a way to write a simple tool that will automatically show you the entire interface. Here’s the way it works:
```java
//: typeinfo/ShowMethods.java
// Using reflection to show all the methods of a class,
// even if the methods are defined in the base class.
// {Args: ShowMethods}
import java.lang.reflect.*;
import java.util.regex.*;
import static net.mindview.util.Print.*;
public class ShowMethods {
private static String usage =
```

<!--p441-->
1Especially in the past. However, Sun has greatly improved its HTML Java documentation so that it’s easier to see base- class methods.
```java
"usage:\n" +
"ShowMethods qualified.class.name\n" +
"To show all methods in class or:\n" +
"ShowMethods qualified.class.name word\n" +
"To search for methods involving ‘word’";
private static Pattern p = Pattern.compile("\\w+\\.");
public static void main(String[] args) {
if(args.length < 1) {
print(usage);
System.exit(0);
}
int lines = 0;
try {
Class<?> c = Class.forName(args[0]);
Method[] methods = c.getMethods();
Constructor[] ctors = c.getConstructors();
if(args.length == 1) {
for(Method method : methods)
print(
p.matcher(method.toString()).replaceAll(""));
for(Constructor ctor : ctors)
print(p.matcher(ctor.toString()).replaceAll(""));
lines = methods.length + ctors.length;
} else {
for(Method method : methods)
if(method.toString().indexOf(args[1]) != -1) {
print(
p.matcher(method.toString()).replaceAll(""));
lines++;
}
for(Constructor ctor : ctors)
if(ctor.toString().indexOf(args[1]) != -1) {
print(p.matcher(
ctor.toString()).replaceAll(""));
lines++;
}
}
} catch(ClassNotFoundException e) {
print("No such class: " + e);
}
}
} /* Output:
public static void main(String[])
public native int hashCode()
public final native Class getClass()
public final void wait(long,int) throws InterruptedException
public final void wait() throws InterruptedException
public final native void wait(long) throws InterruptedException
public boolean equals(Object)
public String toString()
public final native void notify()
public final native void notifyAll()
public ShowMethods()
*///:~
```

<!--p442-->
The Class methods getMethods( ) and getConstructors( ) return an array of Method and array of Constructor, respectively. Each of these classes has further methods to dissect the names, arguments, and return values of the methods they represent. But you can also just use toString( ), as is done here, to produce a String with the entire method signature. The rest of the code extracts the command-line information, determines if a particular signature matches your target string (using indexOf( )), and strips off the name qualifiers using regular expressions (introduced in the Strings chapter). Type Information The result produced by Class.forName( ) cannot be known at compile time, and therefore all the method signature information is being extracted at run time. If you investigate the JDK reflection documentation, you’ll see that there is enough support to actually set up and make a method call on an object that’s totally unknown at compile time (there will be examples of this later in this book). Although initially this is something you may not think you’ll ever need, the value of full reflection can be quite surprising. The output above is produced from the command line:
```java
java ShowMethods ShowMethods
```
You can see that the output includes a public default constructor, even though no constructor was defined. The constructor you see is the one that’s automatically synthesized by the compiler. If you then make ShowMethods a non-public class (that is, package access), the synthesized default constructor no longer shows up in the output. The synthesized default constructor is automatically given the same access as the class. Another interesting experiment is to invoke Java ShowMethods java.lang.String with an extra argument of char, int, String, etc. This tool can be a real time-saver while you’re programming, when you can’t remember if a class has a particular method and you don’t want to go hunting through the index or class hierarchy in the JDK documentation, or if you don’t know whether that class can do anything with, for example, Color objects. The Graphical User Interfaces chapter contains a GUI version of this program (customized to extract information for Swing components) so you can leave it running while you’re writing code, to allow quick lookups. Exercise 17:(2) Modify the regular expression in ShowMethods.java to additionally strip off the keywords native and final (hint: use the OR operator’|’)- Exercise 18:(1) Make ShowMethods a non-public class and verify that the synthesized default constructor no longer shows up in the output. Exercise 19: (4) In ToyTest.java, use reflection to create a Toy object using the non- default constructor. Exercise 20:(5) Look up the interface for java.lang.Class in the JDK documentation from http://java.sun.com. Write a program that takes the name of a class as a command-line argument, then uses the Class methods to dump all the information available for that class. Test your program with a standard library class and a class you create. Dynamic proxies Proxy is one of the basic design patterns. It is an object that you insert in place of the "real" object in order to provide additional or different operations—these usually involve communication with a "real" object, so a proxy typically acts as a go-between. Here’s a trivial example to show the structure of a proxy:

<!--p443-->
```java
//: typeinfo/SimpleProxyDemo.java
import static net.mindview.util.Print.*;
interface Interface {
void doSomething();
void somethingElse(String arg);
}
class RealObject implements Interface {
public void doSomething() { print("doSomething"); }
public void somethingElse(String arg) {
print("somethingElse " + arg);
}
}
class SimpleProxy implements Interface {
private Interface proxied;
public SimpleProxy(Interface proxied) {
this.proxied = proxied;
}
public void doSomething() {
print("SimpleProxy doSomething");
proxied.doSomething();
}
public void somethingElse(String arg) {
print("SimpleProxy somethingElse " + arg);
proxied.somethingElse(arg);
}
}
class SimpleProxyDemo {
public static void consumer(Interface iface) {
iface.doSomething();
iface.somethingElse("bonobo");
}
public static void main(String[] args) {
consumer(new RealObject());
consumer(new SimpleProxy(new RealObject()));
}
} /* Output:
doSomething
somethingElse bonobo
SimpleProxy doSomething
doSomething
SimpleProxy somethingElse bonobo
somethingElse bonobo
*///:~
```

<!--p444-->
Because consumer( ) accepts an Interface, it can’t know if it’s getting a RealObject or a SimpleProxy, because both implement Interface. But the SimpleProxy inserted between the client and the RealObject performs operations and then calls the identical method on a RealObject. A proxy can be helpful anytime you’d like to separate extra operations into a different place than the "real object," and especially when you want to easily change from not using the extra operations to using them, and vice versa (the point of design patterns is to encapsulate change—so you need to be changing things in order to justify the pattern). For example, what if you wanted to track calls to the methods in the RealObject, or to measure the overhead of such calls? This is not code you want to have incorporated in your application, so a proxy allows you to add and remove it easily. Java’s dynamic proxy takes the idea of a proxy one step further, by both creating the proxy object dynamically and handling calls to the proxied methods dynamically. All calls made on a dynamic proxy are redirected to a single invocation handler, which has the job of discovering what the call is and deciding what to do about it. Here’s SimpleProxyDemo.java rewritten to use a dynamic proxy: Type Information
```java
//: typeinfo/SimpleDynamicProxy.java
import java.lang.reflect.*;
class DynamicProxyHandler implements InvocationHandler {
private Object proxied;
public DynamicProxyHandler(Object proxied) {
this.proxied = proxied;
}
public Object
invoke(Object proxy, Method method, Object[] args)
throws Throwable {
System.out.println("**** proxy: " + proxy.getClass() +
", method: " + method + ", args: " + args);
if(args != null)
for(Object arg : args)
System.out.println(" " + arg);
return method.invoke(proxied, args);
}
}
class SimpleDynamicProxy {
public static void consumer(Interface iface) {
iface.doSomething();
iface.somethingElse("bonobo");
}
public static void main(String[] args) {
RealObject real = new RealObject();
consumer(real);
// Insert a proxy and call again:
Interface proxy = (Interface)Proxy.newProxyInstance(
Interface.class.getClassLoader(),
new Class[]{ Interface.class },
new DynamicProxyHandler(real));
consumer(proxy);
}
} /* Output: (95% match)
doSomething
somethingElse bonobo
**** proxy: class $Proxy0, method: public abstract void
Interface.doSomething(), args: null
doSomething
**** proxy: class $Proxy0, method: public abstract void
Interface.somethingElse(java.lang.String), args:
[Ljava.lang.Object;@42e816
bonobo
somethingElse bonobo
*///:~
```

<!--p445-->
You create a dynamic proxy by calling the static method Proxy.newProxyInstance( ), which requires a class loader (you can generally just hand it a class loader from an object that has already been loaded), a list of interfaces (not classes or abstract classes) that you wish the proxy to implement, and an implementation of the interface InvocationHandler. The dynamic proxy will redirect all calls to the invocation handler, so the constructor for the invocation handler is usually given the reference to the "real" object so that it can forward requests once it performs its intermediary task. The invoke( ) method is handed the proxy object, in case you need to distinguish where the request came from—but in many cases you won’t care. However, be careful when calling methods on the proxy inside invoke( ), because calls through the interface are redirected through the proxy. In general you will perform the proxied operation and then use Method.invoke( ) to forward the request to the proxied object, passing the necessary arguments. This may initially seem limiting, as if you can only perform generic operations. However, you can filter for certain method calls, while passing others through:
```java
//: typeinfo/SelectingMethods.java
// Looking for particular methods in a dynamic proxy.
import java.lang.reflect.*;
import static net.mindview.util.Print.*;
class MethodSelector implements InvocationHandler {
private Object proxied;
public MethodSelector(Object proxied) {
this.proxied = proxied;
}
public Object
invoke(Object proxy, Method method, Object[] args)
throws Throwable {
if(method.getName().equals("interesting"))
print("Proxy detected the interesting method");
return method.invoke(proxied, args);
}
}
interface SomeMethods {
void boring1();
void boring2();
void interesting(String arg);
void boring3();
}
class Implementation implements SomeMethods {
public void boring1() { print("boring1"); }
public void boring2() { print("boring2"); }
public void interesting(String arg) {
print("interesting " + arg);
}
public void boring3() { print("boring3"); }
}
class SelectingMethods {
public static void main(String[] args) {
SomeMethods proxy= (SomeMethods)Proxy.newProxyInstance(
SomeMethods.class.getClassLoader(),
new Class[]{ SomeMethods.class },
new MethodSelector(new Implementation()));
proxy.boring1();
proxy.boring2();
proxy.interesting("bonobo");
proxy.boring3();
}
} /* Output:
boring1
boring2
Proxy detected the interesting method
interesting bonobo
boring3
*///:~
```

<!--p446-->
Here, we are just looking for method names, but you could also be looking for other aspects of the method signature, and you could even search for particular argument values. Type Information The dynamic proxy is not a tool that you’ll use every day, but it can solve certain types of problems very nicely. You can learn more about Proxy and other design patterns in Thinking in Patterns (see www.MindView.net) and Design Patterns, by Erich Gamma et al. (Addison- Wesley, 1995). Exercise 21:(3) Modify SimpleProxyDemo.java so that it measures method-call times. Exercise 22:(3) Modify SimpleDynamicProxy.java so that it measures method-call times. Exercise 23:(3) Inside invoke( ) in SimpleDynamicProxy.java, try to print the proxy argument and explain what happens. Project:2Write a system using dynamic proxies to implement transactions, where the proxy performs a commit if the proxied call is successful (doesn’t throw any exceptions) and a rollback if it fails. Your commit and rollback should work on an external text file, which is outside the control of Java exceptions. You will have to pay attention to the atomicity of operations. Null Objects When you use the built-in null to indicate the absence of an object, you must test a reference for null-ness every time you use it. This can get very tedious and produce ponderous code. The problem is that null has no behavior of its own except for producing a NullPointerException if you try to do anything with it. Sometimes it is useful to introduce the idea of a Null Object3that will accept messages for the object that it’s "standing in" for, but will return values indicating that no "real" object is actually there. This way, you can assume that all objects are valid and you don’t have to waste programming time checking for null (and reading the resulting code). Although it’s fun to imagine a programming language that would automatically create Null Objects for you, in practice it doesn’t make sense to use them everywhere—sometimes checking for null is fine, and sometimes you can reasonably assume that you won’t encounter null, and sometimes even detecting aberrations via NullPointerException is acceptable. The place where Null Objects seem to be most useful is "closer to the data," with objects that represent entities in the problem space. As a simple example, many systems will have a Person class, and there are situations in the code where you don’t have an actual person (or you do, but you don’t have all the information about that person yet), so traditionally you’d use a null reference and test for it. Instead, we can make a Null Object. But even though the Null Object will respond to all messages that the "real" object will respond to, you still need a way to test for nullness. The simplest way to do this is to create a tagging interface:
```java
//: net/mindview/util/Null.java
package net.mindview.util;
public interface Null {} ///:~
```

<!--p447-->
2Projects are suggestions to be used (for example) as term projects. Solutions to projects are not included in the solution guide. 3Discovered by Bobby Woolf and Bruce Anderson. This can be seen as a special case of the Strategy pattern. A variant of Null Object is the Null Iterator pattern, which makes iteration over the nodes in a composite hierarchy transparent to the client (the client can then use the same logic for iterating over the composite and leaf nodes). This allows instanceof to detect the Null Object, and more importantly, does not require you to add an isNull( ) method to all your classes (which would be, after all, just a different way of performing RTTI—why not use the built-in facility instead?).
```java
//: typeinfo/Person.java
// A class with a Null Object.
import net.mindview.util.*;
class Person {
public final String first;
public final String last;
public final String address;
// etc.
public Person(String first, String last, String address){
this.first = first;
this.last = last;
this.address = address;
}
public String toString() {
return "Person: " + first + " " + last + " " + address;
}
public static class NullPerson
extends Person implements Null {
private NullPerson() { super("None", "None", "None"); }
public String toString() { return "NullPerson"; }
}
public static final Person NULL = new NullPerson();
} ///:~
```
In general, the Null Object will be a Singleton, so here it is created as a static final instance. This works because Person is immutable—you can only set the values in the constructor, and then read those values, but you can’t modify them (because Strings themselves are inherently immutable). If you want to change a NullPerson, you can only replace it with a new Person object. Notice that you have the option of detecting the generic Null or the more specific NullPerson using instanceof, but with the Singleton approach you can also just use equals( ) or even == to compare to Person.NULL. Now suppose you’re back in the high-flying days of Internet startups and you’ve been given a big pile of venture funding for your Amazing Idea. You’re ready to staff up, but while you’re waiting for positions to be filled, you can use Person Null Objects as placeholders for each Position:
```java
//: typeinfo/Position.java
class Position {
private String title;
private Person person;
public Position(String jobTitle, Person employee) {
title = jobTitle;
person = employee;
if(person == null)
person = Person.NULL;
}
public Position(String jobTitle) {
title = jobTitle;
person = Person.NULL;
}
public String getTitle() { return title; }
public void setTitle(String newTitle) {
title = newTitle;
}
```

<!--p448-->
Type Information
```java
public Person getPerson() { return person; }
public void setPerson(Person newPerson) {
person = newPerson;
if(person == null)
person = Person.NULL;
}
public String toString() {
return "Position: " + title + " " + person;
}
} ///:~
```
With Position, we don’t need to make a Null Object because the existence of Person.NULL implies a null Position (it’s possible that, later, you’ll discover the need to add an explicit Null Object for Position, but YAGNI4(You Aren’t Going to Need It) says to try "the simplest thing that could possibly work" for your first draft, and to wait until some aspect of the program requires you to add in the extra feature, rather than assuming it’s necessary). The Staff class can now look for Null Objects when you are filling positions:
```java
//: typeinfo/Staff.java
import java.util.*;
public class Staff extends ArrayList<Position> {
public void add(String title, Person person) {
add(new Position(title, person));
}
public void add(String... titles) {
for(String title : titles)
add(new Position(title));
}
public Staff(String... titles) { add(titles); }
public boolean positionAvailable(String title) {
for(Position position : this)
if(position.getTitle().equals(title) &&
position.getPerson() == Person.NULL)
return true;
return false;
}
public void fillPosition(String title, Person hire) {
for(Position position : this)
if(position.getTitle().equals(title) &&
position.getPerson() == Person.NULL) {
position.setPerson(hire);
return;
}
throw new RuntimeException(
"Position " + title + " not available");
}
public static void main(String[] args) {
Staff staff = new Staff("President", "CTO",
"Marketing Manager", "Product Manager",
"Project Lead", "Software Engineer",
"Software Engineer", "Software Engineer",
"Software Engineer", "Test Engineer",
"Technical Writer");
staff.fillPosition("President",
new Person("Me", "Last", "The Top, Lonely At"));
staff.fillPosition("Project Lead",
```

<!--p449-->
4A tenet of Extreme Programming (XP), as is "Do the simplest thing that could possibly work."
```java
new Person("Janet", "Planner", "The Burbs"));
if(staff.positionAvailable("Software Engineer"))
staff.fillPosition("Software Engineer",
new Person("Bob", "Coder", "Bright Light City"));
System.out.println(staff);
}
} /* Output:
[Position: President Person: Me Last The Top, Lonely At, Position: CTO
NullPerson, Position: Marketing Manager NullPerson, Position: Product
Manager NullPerson, Position: Project Lead Person: Janet Planner The
Burbs, Position: Software Engineer Person: Bob Coder Bright Light City,
Position: Software Engineer NullPerson, Position: Software Engineer
NullPerson, Position: Software Engineer NullPerson, Position: Test
Engineer NullPerson, Position: Technical Writer NullPerson]
*///:~
```
Notice that you must still test for Null Objects in some places, which is not that different from checking for null, but in other places (such as toString( ) conversions, in this case), you don’t have to perform extra tests; you can just assume that all object references are valid. If you are working with interfaces instead of concrete classes, it’s possible to use a DynamicProxy to automatically create the Null Objects. Suppose we have a Robot interface that defines a name, model, and a List < Operation > that describes what the Robot is capable of doing. Operation contains a description and a command (it’s a type of Command pattern):
```java
//: typeinfo/Operation.java
public interface Operation {
String description();
void command();
} ///:~
```
You can access a Robot’s services by calling operations( ):
```java
//: typeinfo/Robot.java
import java.util.*;
import net.mindview.util.*;
public interface Robot {
String name();
String model();
List<Operation> operations();
class Test {
public static void test(Robot r) {
if(r instanceof Null)
System.out.println("[Null Robot]");
System.out.println("Robot name: " + r.name());
System.out.println("Robot model: " + r.model());
for(Operation operation : r.operations()) {
System.out.println(operation.description());
operation.command();
}
}
}
} ///:~
```

<!--p450-->
This also incorporates a nested class to perform tests. We can now create a Robot that removes snow: Type Information
```java
//: typeinfo/SnowRemovalRobot.java
import java.util.*;
public class SnowRemovalRobot implements Robot {
private String name;
public SnowRemovalRobot(String name) {this.name = name;}
public String name() { return name; }
public String model() { return "SnowBot Series 11"; }
public List<Operation> operations() {
return Arrays.asList(
new Operation() {
public String description() {
return name + " can shovel snow";
}
public void command() {
System.out.println(name + " shoveling snow");
}
},
new Operation() {
public String description() {
return name + " can chip ice";
}
public void command() {
System.out.println(name + " chipping ice");
}
},
new Operation() {
public String description() {
return name + " can clear the roof";
}
public void command() {
System.out.println(name + " clearing roof");
}
}
);
}
public static void main(String[] args) {
Robot.Test.test(new SnowRemovalRobot("Slusher"));
}
} /* Output:
Robot name: Slusher
Robot model: SnowBot Series 11
Slusher can shovel snow
Slusher shoveling snow
Slusher can chip ice
Slusher chipping ice
Slusher can clear the roof
Slusher clearing roof
*///:~
```
There will presumably be many different types of Robot, and we’d like to have each Null Object do something special for each Robot type—in this case, incorporate information about the exact type of Robot the Null Object is standing for. This information will be captured by the dynamic proxy:

<!--p451-->
```java
//: typeinfo/NullRobot.java
// Using a dynamic proxy to create a Null Object.
import java.lang.reflect.*;
import java.util.*;
import net.mindview.util.*;
class NullRobotProxyHandler implements InvocationHandler {
private String nullName;
private Robot proxied = new NRobot();
NullRobotProxyHandler(Class<? extends Robot> type) {
nullName = type.getSimpleName() + " NullRobot";
}
private class NRobot implements Null, Robot {
public String name() { return nullName; }
public String model() { return nullName; }
public List<Operation> operations() {
return Collections.emptyList();
}
}
public Object
invoke(Object proxy, Method method, Object[] args)
throws Throwable {
return method.invoke(proxied, args);
}
}
public class NullRobot {
public static Robot
newNullRobot(Class<? extends Robot> type) {
return (Robot)Proxy.newProxyInstance(
NullRobot.class.getClassLoader(),
new Class[]{ Null.class, Robot.class },
new NullRobotProxyHandler(type));
}
public static void main(String[] args) {
Robot[] bots = {
new SnowRemovalRobot("SnowBee"),
newNullRobot(SnowRemovalRobot.class)
};
for(Robot bot : bots)
Robot.Test.test(bot);
}
} /* Output:
Robot name: SnowBee
Robot model: SnowBot Series 11
SnowBee can shovel snow
SnowBee shoveling snow
SnowBee can chip ice
SnowBee chipping ice
SnowBee can clear the roof
SnowBee clearing roof
[Null Robot]
Robot name: SnowRemovalRobot NullRobot
Robot model: SnowRemovalRobot NullRobot
*///:~
```

<!--p452-->
Whenever you need a null Robot object, you just call newNullRobot( ), passing the type of Robot you want a proxy for. The proxy fulfills the requirements of the Robot and Null interfaces, and provides the specific name of the type that it proxies. Mock Objects & Stubs Logical variations of the Null Object are the MocA: Object and the Stub. Like Null Object, both of these are stand-ins for the "real" object that will be used in the finished program. However, both Mock Object and Stub pretend to be live objects that deliver real information, rather than being a more intelligent placeholder for null, as Null Object is. Type Information The distinction between Mock Object and Stub is one of degree. Mock Objects tend to be lightweight and self-testing, and usually many of them are created to handle various testing situations. Stubs just return stubbed data, are typically heavyweight and are often reused between tests. Stubs can be configured to change depending on how they are called. So a Stub is a sophisticated object that does lots of things, whereas you usually create lots of small, simple Mock Objects if you need to do many things. Exercise 24:(4) Add Null Objects to RegisteredFactories.java. Interfaces and type information An important goal of the interface keyword is to allow the programmer to isolate components, and thus reduce coupling. If you write to interfaces, you accomplish this, but with type information it’s possible to get around that— interfaces are not airtight guarantees of decoupling. Here’s an example, starting with an interface:
```java
//: typeinfo/interfacea/A.java
package typeinfo.interfacea;
public interface A {
void f();
} ///:~
```
This interface is then implemented, and you can see how to sneak around to the actual implementation type:
```java
//: typeinfo/InterfaceViolation.java
// Sneaking around an interface.
import typeinfo.interfacea.*;
class B implements A {
public void f() {}
public void g() {}
}
public class InterfaceViolation {
public static void main(String[] args) {
A a = new B();
a.f();
// a.g(); // Compile error
System.out.println(a.getClass().getName());
if(a instanceof B) {
B b = (B)a;
b.g();
}
}
} /* Output:
B
*///:~
```

<!--p453-->
Using RTTI, we discover that a has been implemented as a B. By casting to B, we can call a method that’s not in A. Type Information This is perfectly legal and acceptable, but you may not want client programmers to do this, because it gives them an opportunity to couple more closely to your code than you’d like. That is, you may think that the interface keyword is protecting you, but it isn’t, and the fact that you’re using B to implement A in this case is effectively a matter of public record.5 One solution is to simply say that programmers are on their own if they decide to use the actual class rather than the interface. This is probably reasonable in many cases, but if "probably" isn’t enough, you might want to apply more stringent controls. The easiest approach is to use package access for the implementation, so that clients outside the package may not see it:
```java
//: typeinfo/packageaccess/HiddenC.java
package typeinfo.packageaccess;
import typeinfo.interfacea.*;
import static net.mindview.util.Print.*;
class C implements A {
public void f() { print("public C.f()"); }
public void g() { print("public C.g()"); }
void u() { print("package C.u()"); }
protected void v() { print("protected C.v()"); }
private void w() { print("private C.w()"); }
}
public class HiddenC {
public static A makeA() { return new C(); }
} ///:~
```
The only public part of this package, HiddenC, produces an A interface when you call it. What’s interesting about this is that even if you were to return a C from makeA( ), you still couldn’t use anything but an A from outside the package, since you cannot name C outside the package. Now if you try to downcast to C, you can’t do it because there is no ‘C type available outside the package:
```java
//: typeinfo/HiddenImplementation.java
// Sneaking around package access.
import typeinfo.interfacea.*;
import typeinfo.packageaccess.*;
import java.lang.reflect.*;
public class HiddenImplementation {
public static void main(String[] args) throws Exception {
A a = HiddenC.makeA();
a.f();
System.out.println(a.getClass().getName());
// Compile error: cannot find symbol ‘C’:
/* if(a instanceof C) {
C c = (C)a;
c.g();
} */
// Oops! Reflection still allows us to call g():
callHiddenMethod(a, "g");
```

<!--p454-->
5The most famous case of this is the Windows operating system, which had a published API that you were supposed to write to, and an unpublished but visible set of functions that you could discover and call. To solve problems, programmers used the hidden API functions, which forced Microsoft to maintain them as if they were part of the public API. This became a source of great cost and effort for the company.
```java
// And even methods that are less accessible!
callHiddenMethod(a, "u");
callHiddenMethod(a, "v");
callHiddenMethod(a, "w");
}
static void callHiddenMethod(Object a, String methodName)
throws Exception {
Method g = a.getClass().getDeclaredMethod(methodName);
g.setAccessible(true);
g.invoke(a);
}
} /* Output:
public C.f()
typeinfo.packageaccess.C
public C.g()
package C.u()
protected C.v()
private C.w()
*///:~
```
As you can see, it’s still possible to reach in and call all of the methods using reflection, even private methods! If you know the name of the method, you can call setAccessible(true) on the Method object to make it callable, as seen in callHiddenMethod( ). You may think that you can prevent this by only distributing compiled code, but that’s no solution. All you must do is run javap, which is the decompiler that comes with the JDK. Here’s the command line:
```java
javap -private C
```
The -private flag indicates that all members should be displayed, even private ones. Here’s the output:
```java
class typeinfo.packageaccess.C extends
java.lang.Object implements typeinfo.interfacea.A {
typeinfo.packageaccess.C();
public void f( );
public void g( );
void u( );
protected void v( );
private void w();
}
```
So anyone can get the names and signatures of your most private methods, and call them. What if you implement the interface as a private inner class? Here’s what it looks like:

<!--p455-->
```java
//: typeinfo/InnerImplementation.java
// Private inner classes can’t hide from reflection.
import typeinfo.interfacea.*;
import static net.mindview.util.Print.*;
class InnerA {
private static class C implements A {
public void f() { print("public C.f()"); }
public void g() { print("public C.g()"); }
void u() { print("package C.u()"); }
protected void v() { print("protected C.v()"); }
private void w() { print("private C.w()"); }
}
public static A makeA() { return new C(); }
}
public class InnerImplementation {
public static void main(String[] args) throws Exception {
A a = InnerA.makeA();
a.f();
System.out.println(a.getClass().getName());
// Reflection still gets into the private class:
HiddenImplementation.callHiddenMethod(a, "g");
HiddenImplementation.callHiddenMethod(a, "u");
HiddenImplementation.callHiddenMethod(a, "v");
HiddenImplementation.callHiddenMethod(a, "w");
}
} /* Output:
public C.f()
InnerA$C
public C.g()
package C.u()
protected C.v()
private C.w()
*///:~
```
That didn’t hide anything from reflection. What about an anonymous class?
```java
//: typeinfo/AnonymousImplementation.java
// Anonymous inner classes can’t hide from reflection.
import typeinfo.interfacea.*;
import static net.mindview.util.Print.*;
class AnonymousA {
public static A makeA() {
return new A() {
public void f() { print("public C.f()"); }
public void g() { print("public C.g()"); }
void u() { print("package C.u()"); }
protected void v() { print("protected C.v()"); }
private void w() { print("private C.w()"); }
};
}
}
public class AnonymousImplementation {
public static void main(String[] args) throws Exception {
A a = AnonymousA.makeA();
a.f();
System.out.println(a.getClass().getName());
// Reflection still gets into the anonymous class:
HiddenImplementation.callHiddenMethod(a, "g");
HiddenImplementation.callHiddenMethod(a, "u");
HiddenImplementation.callHiddenMethod(a, "v");
HiddenImplementation.callHiddenMethod(a, "w");
}
} /* Output:
public C.f()
AnonymousA$1
public C.g()
package C.u()
protected C.v()
private C.w()
*///:~
```

<!--p456-->
Type Information There doesn’t seem to be any way to prevent reflection from reaching in and calling methods that have non-public access. This is also true for fields, even private fields:
```java
//: typeinfo/ModifyingPrivateFields.java
import java.lang.reflect.*;
class WithPrivateFinalField {
private int i = 1;
private final String s = "I’m totally safe";
private String s2 = "Am I safe?";
public String toString() {
return "i = " + i + ", " + s + ", " + s2;
}
}
public class ModifyingPrivateFields {
public static void main(String[] args) throws Exception {
WithPrivateFinalField pf = new WithPrivateFinalField();
System.out.println(pf);
Field f = pf.getClass().getDeclaredField("i");
f.setAccessible(true);
System.out.println("f.getInt(pf): " + f.getInt(pf));
f.setInt(pf, 47);
System.out.println(pf);
f = pf.getClass().getDeclaredField("s");
f.setAccessible(true);
System.out.println("f.get(pf): " + f.get(pf));
f.set(pf, "No, you’re not!");
System.out.println(pf);
f = pf.getClass().getDeclaredField("s2");
f.setAccessible(true);
System.out.println("f.get(pf): " + f.get(pf));
f.set(pf, "No, you’re not!");
System.out.println(pf);
}
} /* Output:
i = 1, I’m totally safe, Am I safe?
f.getInt(pf): 1
i = 47, I’m totally safe, Am I safe?
f.get(pf): I’m totally safe
i = 47, I’m totally safe, Am I safe?
f.get(pf): Am I safe?
i = 47, I’m totally safe, No, you’re not!
*///:~
```

<!--p457-->

<!--p458-->

<!--p459-->
However, final fields are actually safe from change. The runtime system accepts any attempts at change without complaint, but nothing actually happens. In general, all these access violations are not the worst thing in the world. If someone uses such a technique to call methods that you marked with private or package access (thus clearly indicating they should not call them), then it’s difficult for them to complain if you change some aspect of those methods. On the other hand, the fact that you always have a back door into a class may allow you to solve certain types of problems that could otherwise be difficult or impossible, and the benefits of reflection in general are undeniable. Exercise 25:(2) Create a class containing private, protected and package-access methods. Write code to access these methods from outside of the class’s package. Type Information Summary RTTI allows you to discover type information from an anonymous base-class reference. Thus, it’s ripe for misuse by the novice, since it might make sense before polymorphic method calls do. For people coming from a procedural background, it’s difficult not to organize programs into sets of switch statements. You can accomplish this with RTTI and thus lose the important value of polymorphism in code development and maintenance. The intent of 0 0 programming is to use polymorphic method calls everywhere you can, and RTTI only when you must. However, using polymorphic method calls as they are intended requires that you have control of the base-class definition, because at some point in the extension of your program you might discover that the base class doesn’t include the method you need. If the base class comes from someone else’s library, one solution is RTTI: You can inherit a new type and add your extra method. Elsewhere in the code you can detect your particular type and call that special method. This doesn’t destroy the polymorphism and extensibility of the program, because adding a new type will not require you to hunt for switch statements in your program. However, when you add code that requires your new feature, you must use RTTI to detect your particular type. Putting a feature in a base class might mean that, for the benefit of one particular class, all of the other classes derived from that base require some meaningless stub of a method. This makes the interface less clear and annoys those who must override abstract methods when they derive from that base class. For example, consider a class hierarchy representing musical instruments. Suppose you want to clear the spit valves of all the appropriate instruments in your orchestra. One option is to put a clearSpitValve( ) method in the base class Instrument, but this is confusing because it implies that Percussion, Stringed and Electronic instruments also have spit valves. RTTI provides a much more reasonable solution because you can place the method in the specific class where it’s appropriate (Wind, in this case). At the same time, you may discover that there’s a more sensible solution—here, a preparelnstrument( ) method in the base class. However, you might not see such a solution when you’re first solving the problem and could mistakenly assume that you must use RTTI. Finally, RTTI will sometimes solve efficiency problems. Suppose your code nicely uses polymorphism, but it turns out that one of your objects reacts to this general-purpose code in a horribly inefficient way. You can pick out that type using RTTI and write case-specific code to improve the efficiency. Be wary, however, of programming for efficiency too soon. It’s a seductive trap. It’s best to get the program working/jrsf, then decide if it’s running fast enough, and only then should you attack efficiency issues—with a profiler (see the supplement at http://MindView.net/Books/BetterJava). We’ve also seen that reflection opens up a new world of programming possibilities by allowing a much more dynamic style of programming. There are some for whom the dynamic nature of reflection is disturbing. The fact that you can do things that can only be checked at run time and reported with exceptions seems, to a mind grown comfortable with the security of static type checking, to be the wrong direction. Some people go so far as to say that introducing the possibility of a runtime exception is a clear indicator that such code should be avoided. I find that this sense of security is an illusionthere are always things that can happen at run time and throw exceptions, even in a program that contains no try blocks or exception specifications. Instead, I think that the existence of a consistent error-reporting model empowers us to write dynamic code using reflection. Of course it’s worth trying to write code that can be statically checked ... when you can. But I believe that dynamic code is one of the important facilities that separate Java from languages like C++. Exercise 26:(3) Implement clearSpitValve( ) as described in the summary. Type Information Solutions to selected exercises can be found in the electronic document The Thinking in Java Annotated Solution Guide, available for sale from www.MindView.net.