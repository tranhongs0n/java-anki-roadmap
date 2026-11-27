# 19. Enumerated Types (printed p725-760)


<!--p747-->
Enumerated Types
## The enum keyword allows you to create a new type with a restricted
set of named values, and to treat those values as regular program components. This turns out to be very useful.1 Enumerations were introduced briefly at the end of Initialization & Cleanup. However, now that you understand some of the deeper issues in Java, we can take a more detailed look at the Java SE5 enumeration feature. You’ll see that there are some very interesting things that you can do with enums, but this chapter should also give you more insight into other language features that you’ve now seen, such as generics and reflection. You’ll also learn a few more design patterns.
## Basic enum features
As shown in Initialization & Cleanup, you can step through the list of enum constants by calling values( ) on the enum. The values( ) method produces an array of the enum constants in the order in which they were declared, so you can use the resulting array in (for example) a foreach loop. When you create an enum, an associated class is produced for you by the compiler. This class is automatically inherited from java.lang.Enum, which provides certain capabilities that you can see in this example:
```java
//: enumerated/EnumClass.java
// Capabilities of the Enum class
import static net.mindview.util.Print.*;
enum Shrubbery { GROUND, CRAWLING, HANGING }
public class EnumClass {
public static void main(String[] args) {
for(Shrubbery s : Shrubbery.values()) {
print(s + " ordinal: " + s.ordinal());
printnb(s.compareTo(Shrubbery.CRAWLING) + " ");
printnb(s.equals(Shrubbery.CRAWLING) + " ");
print(s == Shrubbery.CRAWLING);
print(s.getDeclaringClass());
print(s.name());
print("----------------------");
}
// Produce an enum value from a string name:
for(String s : "HANGING CRAWLING GROUND".split(" ")) {
Shrubbery shrub = Enum.valueOf(Shrubbery.class, s);
print(shrub);
}
}
} /* Output:
GROUND ordinal: 0
-1 false false
class Shrubbery
```

<!--p748-->
1 Joshua Bloch was extremely helpful in developing this chapter.
```java
GROUND
----------------------
CRAWLING ordinal: 1
0 true true
class Shrubbery
CRAWLING
----------------------
HANGING ordinal: 2
1 false false
class Shrubbery
HANGING
----------------------
HANGING
CRAWLING
GROUND
*///:~
```
The ordinal( ) method produces an int indicating the declaration order of each enum instance, starting from zero. You can always safely compare enum instances using ==, and equals( ) and hashCode( ) are automatically created for you. The Enum class is Comparable, so there’s a compareTo( ) method, and it is also Serializable. If you call getDeclaringClass( ) on an enum instance, you’ll find out the enclosing enum class. The name( ) method produces the name exactly as it is declared, and this is what you get with toString( ), as well. valueOf( ) is a static member of Enum, and produces the enum instance that corresponds to the String name you pass to it, or throws an exception if there’s no match.
## Using static imports with enums
Consider a variation of Burrito.java from the Initialization & Cleanup chapter:

<!--p749-->
```java
//: enumerated/Spiciness.java
package enumerated;
public enum Spiciness {
NOT, MILD, MEDIUM, HOT, FLAMING
} ///:~
//: enumerated/Burrito.java
package enumerated;
import static enumerated.Spiciness.*;
public class Burrito {
Spiciness degree;
public Burrito(Spiciness degree) { this.degree = degree;}
public String toString() { return "Burrito is "+ degree;}
public static void main(String[] args) {
System.out.println(new Burrito(NOT));
System.out.println(new Burrito(MEDIUM));
System.out.println(new Burrito(HOT));
}
} /* Output:
Burrito is NOT
Burrito is MEDIUM
Burrito is HOT
*///:~
```
The static import brings all the enum instance identifiers into the local namespace, so they don’t need to be qualified. Is this a good idea, or is it better to be explicit and qualify all enum instances? It probably depends on the complexity of your code. The compiler certainly won’t let you use the wrong type, so your only concern is whether the code will be confusing to the reader. In many situations it will probably be fine but you should evaluate it on an individual basis. Note that it is not possible to use this technique if the enum is defined in the same file or the default package (apparently there were some arguments within Sun about whether to allow this).
## Adding methods to an enum
Except for the fact that you can’t inherit from it, an enum can be treated much like a regular class. This means that you can add methods to an enum. It’s even possible for an enum to have a main( ). You may want to produce different descriptions for an enumeration than the default toString( ), which simply produces the name of that enum instance, as you’ve seen. To do this, you can provide a constructor to capture extra information, and additional methods to provide an extended description, like this:
```java
//: enumerated/OzWitch.java
// The witches in the land of Oz.
import static net.mindview.util.Print.*;
public enum OzWitch {
// Instances must be defined first, before methods:
WEST("Miss Gulch, aka the Wicked Witch of the West"),
NORTH("Glinda, the Good Witch of the North"),
EAST("Wicked Witch of the East, wearer of the Ruby " +
"Slippers, crushed by Dorothy’s house"),
SOUTH("Good by inference, but missing");
private String description;
// Constructor must be package or private access:
private OzWitch(String description) {
this.description = description;
}
public String getDescription() { return description; }
public static void main(String[] args) {
for(OzWitch witch : OzWitch.values())
print(witch + ": " + witch.getDescription());
}
} /* Output:
WEST: Miss Gulch, aka the Wicked Witch of the West
NORTH: Glinda, the Good Witch of the North
EAST: Wicked Witch of the East, wearer of the Ruby Slippers, crushed by
Dorothy’s house
SOUTH: Good by inference, but missing
*///:~
```

<!--p750-->
Notice that if you are going to define methods you must end the sequence of enum instances with a semicolon. Also, Java forces you to define the instances as the first thing in the enum. You’ll get a compile-time error if you try to define them after any of the methods or fields. The constructor and methods have the same form as a regular class, because with a few restrictions this is a regular class. So you can do pretty much anything you want with enums (although you’ll usually keep them pretty ordinary). Enumerated Types Although the constructor has been made private here as an example, it doesn’t make much difference what access you use—the constructor can only be used to create the enum instances that you declare inside the enum definition; the compiler won’t let you use it to create any new instances once the enum definition is complete.
## Overriding enum methods
Here’s another approach to producing different string values for enumerations. In this case, the instance names are OK but we want to reformat them for display. Overriding the toString( ) method for an enum is the same as overriding it for a regular class:
```java
//: enumerated/SpaceShip.java
public enum SpaceShip {
SCOUT, CARGO, TRANSPORT, CRUISER, BATTLESHIP, MOTHERSHIP;
public String toString() {
String id = name();
String lower = id.substring(1).toLowerCase();
return id.charAt(0) + lower;
}
public static void main(String[] args) {
for(SpaceShip s : values()) {
System.out.println(s);
}
}
} /* Output:
Scout
Cargo
Transport
Cruiser
Battleship
Mothership
*///:~
```
The toString( ) method gets the Spaceship name by calling name( ), and modifies the result so that only the first letter is capitalized.
## enums in switch statements
One very convenient capability of enums is the way that they can be used in switch statements. Ordinarily, a switch only works with an integral value, but since enums have an established integral order and the order of an instance can be produced with the ordinal( ) method (apparently the compiler does something like this), enums can be used in switch statements. Although normally you must qualify an enum instance with its type, you do not have to do this in a case statement. Here’s an example that uses an enum to create a little state machine:

<!--p751-->
```java
//: enumerated/TrafficLight.java
// Enums in switch statements.
import static net.mindview.util.Print.*;
// Define an enum type:
enum Signal { GREEN, YELLOW, RED, }
public class TrafficLight {
Signal color = Signal.RED;
public void change() {
switch(color) {
// Note that you don’t have to say Signal.RED
// in the case statement:
case RED: color = Signal.GREEN;
break;
case GREEN: color = Signal.YELLOW;
break;
case YELLOW: color = Signal.RED;
break;
}
}
public String toString() {
return "The traffic light is " + color;
}
public static void main(String[] args) {
TrafficLight t = new TrafficLight();
for(int i = 0; i < 7; i++) {
print(t);
t.change();
}
}
} /* Output:
The traffic light is RED
The traffic light is GREEN
The traffic light is YELLOW
The traffic light is RED
The traffic light is GREEN
The traffic light is YELLOW
The traffic light is RED
*///:~
```
The compiler does not complain that there is no default statement inside the switch, but that’s not because it notices that you have case statements for each Signal instance. If you comment out one of the case statements it still won’t complain. This means you will have to pay attention and ensure that you cover all the cases on your own. On the other hand, if you are calling return from case statements, the compiler will complain if you don’t have a default—even if you’ve covered all the possible values of the enum. Exercise 1:(2) Use a static import to modify TrafficLight.java so you don’t have to qualify the enum instances.
## The mystery of values()
As noted earlier, all enum classes are created for you by the compiler and extend the Enum class. However, if you look at Enum, you’ll see that there is no values( ) method, even though we’ve been using it. Are there any other "hidden" methods? We can write a small reflection program to find out:
```java
//: enumerated/Reflection.java
// Analyzing enums using reflection.
import java.lang.reflect.*;
import java.util.*;
import net.mindview.util.*;
import static net.mindview.util.Print.*;
enum Explore { HERE, THERE }
public class Reflection {
public static Set<String> analyze(Class<?> enumClass) {
print("----- Analyzing " + enumClass + " -----");
```

<!--p752-->
Enumerated Types
```java
print("Interfaces:");
for(Type t : enumClass.getGenericInterfaces())
print(t);
print("Base: " + enumClass.getSuperclass());
print("Methods: ");
Set<String> methods = new TreeSet<String>();
for(Method m : enumClass.getMethods())
methods.add(m.getName());
print(methods);
return methods;
}
public static void main(String[] args) {
Set<String> exploreMethods = analyze(Explore.class);
Set<String> enumMethods = analyze(Enum.class);
print("Explore.containsAll(Enum)? " +
exploreMethods.containsAll(enumMethods));
printnb("Explore.removeAll(Enum): ");
exploreMethods.removeAll(enumMethods);
print(exploreMethods);
// Decompile the code for the enum:
OSExecute.command("javap Explore");
}
} /* Output:
----- Analyzing class Explore -----
Interfaces:
Base: class java.lang.Enum
Methods:
[compareTo, equals, getClass, getDeclaringClass, hashCode, name, notify,
notifyAll, ordinal, toString, valueOf, values, wait]
----- Analyzing class java.lang.Enum -----
Interfaces:
java.lang.Comparable<E>
interface java.io.Serializable
Base: class java.lang.Object
Methods:
[compareTo, equals, getClass, getDeclaringClass, hashCode, name, notify,
notifyAll, ordinal, toString, valueOf, wait]
Explore.containsAll(Enum)? true
Explore.removeAll(Enum): [values]
Compiled from "Reflection.java"
final class Explore extends java.lang.Enum{
public static final Explore HERE;
public static final Explore THERE;
public static final Explore[] values();
public static Explore valueOf(java.lang.String);
static {};
}
*///:~
```

<!--p753-->
So the answer is that values( ) is a static method that is added by the compiler. You can see that valueOf( ) is also added to Explore in the process of creating the enum. This is slightly confusing, because there’s also a valueOf( ) that is part of the Enum class, but that method has two arguments and the added method only has one. However, the use of the Set method here is only looking at method names, and not signatures, so after calling Explore.removeAll(Enum), the only thing that remains is [values]. In the output, you can see that Explore has been made final by the compiler, so you cannot inherit from an enum. There’s also a static initialization clause, which as you’ll see later can be redefined. Because of erasure (described in the Generics chapter), the decompiler does not have full information about Enum, so it shows the base class of Explore as a raw Enum rather than the actual Enum<Explore>. Because values( ) is a static method inserted into the enum definition by the compiler, if you upcast an enum type to Enum, the values( ) method will not be available. Notice, however, that there is a getEnumConstants( ) method in Class, so even if values( ) is not part of the interface of Enum, you can still get the enum instances via the Class object:
```java
//: enumerated/UpcastEnum.java
// No values() method if you upcast an enum
enum Search { HITHER, YON }
public class UpcastEnum {
public static void main(String[] args) {
Search[] vals = Search.values();
Enum e = Search.HITHER; // Upcast
// e.values(); // No values() in Enum
for(Enum en : e.getClass().getEnumConstants())
System.out.println(en);
}
} /* Output:
HITHER
YON
*///:~
```
Because getEnumConstants( ) is a method of Class, you can call it for a class that has no enumerations:
```java
//: enumerated/NonEnum.java
public class NonEnum {
public static void main(String[] args) {
Class<Integer> intClass = Integer.class;
try {
for(Object en : intClass.getEnumConstants())
System.out.println(en);
} catch(Exception e) {
System.out.println(e);
}
}
} /* Output:
java.lang.NullPointerException
*///:~
```

<!--p754-->
However, the method returns null, so you get an exception if you try to use the result. Enumerated Types Implements, not inherits We’ve established that all enums extend java.lang.Enum. Since Java does not support multiple inheritance, this means that you cannot create an enum via inheritance:
```java
enum NotPossible extends Pet { ... // Won’t work
```
However, it is possible to create an enum that implements one or more interfaces:
```java
//: enumerated/cartoons/EnumImplementation.java
// An enum can implement an interface
package enumerated.cartoons;
import java.util.*;
import net.mindview.util.*;
enum CartoonCharacter
implements Generator<CartoonCharacter> {
SLAPPY, SPANKY, PUNCHY, SILLY, BOUNCY, NUTTY, BOB;
private Random rand = new Random(47);
public CartoonCharacter next() {
return values()[rand.nextInt(values().length)];
}
}
public class EnumImplementation {
public static <T> void printNext(Generator<T> rg) {
System.out.print(rg.next() + ", ");
}
public static void main(String[] args) {
// Choose any instance:
CartoonCharacter cc = CartoonCharacter.BOB;
for(int i = 0; i < 10; i++)
printNext(cc);
}
} /* Output:
BOB, PUNCHY, BOB, SPANKY, NUTTY, PUNCHY, SLAPPY, NUTTY, NUTTY, SLAPPY,
*///:~
```
The result is slightly odd, because to call a method you must have an instance of the enum to call it on. However, a CartoonCharacter can now be accepted by any method that takes a Generator; for example, printNext( ). Exercise 2: (2) Instead of implementing an interface, make next( ) a static method. What are the benefits and drawbacks of this approach? Random selection Many of the examples in this chapter require random selection from among enum instances, as you saw in CartoonCharacter.next( ). It’s possible to generalize this task using generics and put the result in the common library:

<!--p755-->
```java
//: net/mindview/util/Enums.java
package net.mindview.util;
import java.util.*;
public class Enums {
private static Random rand = new Random(47);
public static <T extends Enum<T>> T random(Class<T> ec) {
return random(ec.getEnumConstants());
}
public static <T> T random(T[] values) {
return values[rand.nextInt(values.length)];
}
} ///:~
```
The rather odd syntax <T extends Enum<T>> describes T as an enum instance. By passing in Class<T>, we make the class object available, and the array of enum instances can thus be produced. The overloaded random( ) method only needs to know that it is getting a T[] because it doesn’t need to perform Enum operations; it only needs to select an array element at random. The return type is the exact type of the enum. Here’s a simple test of the random( ) method:
```java
//: enumerated/RandomTest.java
import net.mindview.util.*;
enum Activity { SITTING, LYING, STANDING, HOPPING,
RUNNING, DODGING, JUMPING, FALLING, FLYING }
public class RandomTest {
public static void main(String[] args) {
for(int i = 0; i < 20; i++)
System.out.print(Enums.random(Activity.class) + " ");
}
} /* Output:
STANDING FLYING RUNNING STANDING RUNNING STANDING LYING DODGING SITTING
RUNNING HOPPING HOPPING HOPPING RUNNING STANDING LYING FALLING RUNNING
FLYING LYING
*///:~
```

<!--p756-->
Although Enums is a small class, you’ll see that it prevents a fair amount of duplication in this chapter. Duplication tends to produce mistakes, so eliminating duplication is a useful pursuit. Enumerated Types Using interfaces for organization The inability to inherit from an enum can be a bit frustrating at times. The motivation for inheriting from an enum comes partly from wanting to extend the number of elements in the original enum, and partly from wanting to create subcategories by using subtypes. You can achieve categorization by grouping the elements together inside an interface and creating an enumeration based on that interface. For example, suppose you have different classes of food that you’d like to create as enums, but you’d still like each one to be a type of Food. Here’s what it looks like:
```java
//: enumerated/menu/Food.java
// Subcategorization of enums within interfaces.
package enumerated.menu;
public interface Food {
enum Appetizer implements Food {
SALAD, SOUP, SPRING_ROLLS;
}
enum MainCourse implements Food {
LASAGNE, BURRITO, PAD_THAI,
LENTILS, HUMMOUS, VINDALOO;
}
enum Dessert implements Food {
TIRAMISU, GELATO, BLACK_FOREST_CAKE,
FRUIT, CREME_CARAMEL;
}
enum Coffee implements Food {
BLACK_COFFEE, DECAF_COFFEE, ESPRESSO,
LATTE, CAPPUCCINO, TEA, HERB_TEA;
}
} ///:~
```
Since the only subtyping available for an enum is that of interface implementation, each nested enum implements the surrounding interface Food. Now it’s possible to say that "everything is a type of Food" as you can see here:
```java
//: enumerated/menu/TypeOfFood.java
package enumerated.menu;
import static enumerated.menu.Food.*;
public class TypeOfFood {
public static void main(String[] args) {
Food food = Appetizer.SALAD;
food = MainCourse.LASAGNE;
food = Dessert.GELATO;
food = Coffee.CAPPUCCINO;
}
} ///:~
```
The upcast to Food works for each enum type that implements Food, so they are all types of Food. An interface, however, is not as useful as an enum when you want to deal with a set of types. If you want to have an "enum of enums" you can create a surrounding enum with one instance for each enum in Food:

<!--p757-->
```java
//: enumerated/menu/Course.java
package enumerated.menu;
import net.mindview.util.*;
public enum Course {
APPETIZER(Food.Appetizer.class),
MAINCOURSE(Food.MainCourse.class),
DESSERT(Food.Dessert.class),
COFFEE(Food.Coffee.class);
private Food[] values;
private Course(Class<? extends Food> kind) {
values = kind.getEnumConstants();
}
public Food randomSelection() {
return Enums.random(values);
}
} ///:~
```
Each of the above enumstakes the corresponding Class object as a constructor argument, from which it can extract and store all the enum instances using getEnumConstants( ). These instances are later used in randomSelection( ), so now we can create a randomly generated meal by selecting one Food item from each Course:
```java
//: enumerated/menu/Meal.java
package enumerated.menu;
public class Meal {
public static void main(String[] args) {
for(int i = 0; i < 5; i++) {
for(Course course : Course.values()) {
Food food = course.randomSelection();
System.out.println(food);
}
System.out.println("---");
}
}
} /* Output:
SPRING_ROLLS
VINDALOO
FRUIT
DECAF_COFFEE
---
SOUP
VINDALOO
FRUIT
TEA
---
SALAD
BURRITO
FRUIT
TEA
---
SALAD
BURRITO
CREME_CARAMEL
LATTE
---
SOUP
BURRITO
TIRAMISU
ESPRESSO
---
*///:~
```

<!--p758-->
Enumerated Types In this case, the value of creating an enum of enumsis to iterate through each Course. Later, in the VendingMachine.java example, you’ll see another approach to categorization which is dictated by different constraints. Another, more compact, approach to the problem of categorization is to nest enumswithin enums, like this:
```java
//: enumerated/SecurityCategory.java
// More succinct subcategorization of enums.
import net.mindview.util.*;
enum SecurityCategory {
STOCK(Security.Stock.class), BOND(Security.Bond.class);
Security[] values;
SecurityCategory(Class<? extends Security> kind) {
values = kind.getEnumConstants();
}
interface Security {
enum Stock implements Security { SHORT, LONG, MARGIN }
enum Bond implements Security { MUNICIPAL, JUNK }
}
public Security randomSelection() {
return Enums.random(values);
}
public static void main(String[] args) {
for(int i = 0; i < 10; i++) {
SecurityCategory category =
Enums.random(SecurityCategory.class);
System.out.println(category + ": " +
category.randomSelection());
}
}
} /* Output:
BOND: MUNICIPAL
BOND: MUNICIPAL
STOCK: MARGIN
STOCK: MARGIN
BOND: JUNK
STOCK: SHORT
STOCK: LONG
STOCK: LONG
BOND: MUNICIPAL
BOND: JUNK
*///:~
```
The Security interface is necessary to collect the contained enumstogether as a common type. These are then categorized into the enumswithin SecurityCategory. If we take this approach with the Food example, the result is:

<!--p759-->
```java
//: enumerated/menu/Meal2.java
package enumerated.menu;
import net.mindview.util.*;
public enum Meal2 {
APPETIZER(Food.Appetizer.class),
MAINCOURSE(Food.MainCourse.class),
DESSERT(Food.Dessert.class),
COFFEE(Food.Coffee.class);
private Food[] values;
private Meal2(Class<? extends Food> kind) {
values = kind.getEnumConstants();
}
public interface Food {
enum Appetizer implements Food {
SALAD, SOUP, SPRING_ROLLS;
}
enum MainCourse implements Food {
LASAGNE, BURRITO, PAD_THAI,
LENTILS, HUMMOUS, VINDALOO;
}
enum Dessert implements Food {
TIRAMISU, GELATO, BLACK_FOREST_CAKE,
FRUIT, CREME_CARAMEL;
}
enum Coffee implements Food {
BLACK_COFFEE, DECAF_COFFEE, ESPRESSO,
LATTE, CAPPUCCINO, TEA, HERB_TEA;
}
}
public Food randomSelection() {
return Enums.random(values);
}
public static void main(String[] args) {
for(int i = 0; i < 5; i++) {
for(Meal2 meal : Meal2.values()) {
Food food = meal.randomSelection();
System.out.println(food);
}
System.out.println("---");
}
}
} /* Same output as Meal.java *///:~
```
In the end, it’s only a reorganization of the code but it may produce a clearer structure in some cases. Exercise 3:(1)Add a new Course to Course.java and demonstrate that it works in Meal.java. Exercise 4:(1) Repeat the above exercise for Meal2.java. Exercise 5: (4) Modify control/VowelsAndConsonants.java so that it uses three enum types: VOWEL, SOMETIMES_A_VOWEL, and CONSONANT. The enum constructor should take the various letters that describe that particular category. Hint: Use varargs, and remember that varargs automatically creates an array for you. Exercise 6:(3) Is there any special benefit in nesting Appetizer, MainCourse, Dessert, and Coffee inside Food rather than making them standalone enums that just happen to implement Food?
## Using EnumSet instead of flags

<!--p760-->
A Set is a kind of collection that only allows one of each type of object to be added. Of course, an enum requires that all its members be unique, so it would seem to have set behavior, but since you can’t add or remove elements it’s not very useful as a set. The EnumSet was added to Java SE5 to work in concert with enums to create a replacement for traditional int-based "bit flags." Such flags are used to indicate some kind of on-off information, but you end up manipulating bits rather than concepts, so it’s easy to write confusing code. Enumerated Types The EnumSet is designed for speed, because it must compete effectively with bit flags (operations will be typically much faster than a HashSet). Internally, it is represented by (if possible) a single long that is treated as a bit-vector, so it’s extremely fast and efficient. The benefit is that you now have a much more expressive way to indicate the presence or absence of a binary feature, without having to worry about performance. The elements of an EnumSet must come from a single enum. A possible example uses an enum of positions in a building where alarm sensors are present:
```java
//: enumerated/AlarmPoints.java
package enumerated;
public enum AlarmPoints {
STAIR1, STAIR2, LOBBY, OFFICE1, OFFICE2, OFFICE3,
OFFICE4, BATHROOM, UTILITY, KITCHEN
} ///:~
```
The EnumSet can be used to keep track of the alarm status:
```java
//: enumerated/EnumSets.java
// Operations on EnumSets
package enumerated;
import java.util.*;
import static enumerated.AlarmPoints.*;
import static net.mindview.util.Print.*;
public class EnumSets {
public static void main(String[] args) {
EnumSet<AlarmPoints> points =
EnumSet.noneOf(AlarmPoints.class); // Empty set
points.add(BATHROOM);
print(points);
points.addAll(EnumSet.of(STAIR1, STAIR2, KITCHEN));
print(points);
points = EnumSet.allOf(AlarmPoints.class);
points.removeAll(EnumSet.of(STAIR1, STAIR2, KITCHEN));
print(points);
points.removeAll(EnumSet.range(OFFICE1, OFFICE4));
print(points);
points = EnumSet.complementOf(points);
print(points);
}
} /* Output:
[BATHROOM]
[STAIR1, STAIR2, BATHROOM, KITCHEN]
[LOBBY, OFFICE1, OFFICE2, OFFICE3, OFFICE4, BATHROOM, UTILITY]
[LOBBY, BATHROOM, UTILITY]
[STAIR1, STAIR2, OFFICE1, OFFICE2, OFFICE3, OFFICE4, KITCHEN]
*///:~
```

<!--p761-->
A static import is used to simplify the use of the enum constants. The method names are fairly self-explanatory, and you can find the full details in the JDK documentation. When you look at this documentation, you’ll see something interesting—the of( ) method has been overloaded both with varargs and with individual methods taking two through five explicit arguments. This is an indication of the concern for performance with EnumSet, because a single of( ) method using varargs could have solved the problem, but it’s slightly less efficient than having explicit arguments. Thus, if you call of( ) with two through five arguments you will get the explicit (slightly faster) method calls, but if you call it with one argument or more than five, you will get the varargs version of of( ). Notice that if you call it with one argument, the compiler will not construct the varargs array and so there is no extra overhead for calling that version with a single argument. EnumSetsare built on top of longs, a long is 64 bits, and each enum instance requires one bit to indicate presence or absence. This means you can have an EnumSet for an enum of up to 64 elements without going beyond the use of a single long. What happens if you have more than 64 elements in your enum?
```java
//: enumerated/BigEnumSet.java
import java.util.*;
public class BigEnumSet {
enum Big { A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10,
A11, A12, A13, A14, A15, A16, A17, A18, A19, A20, A21,
A22, A23, A24, A25, A26, A27, A28, A29, A30, A31, A32,
A33, A34, A35, A36, A37, A38, A39, A40, A41, A42, A43,
A44, A45, A46, A47, A48, A49, A50, A51, A52, A53, A54,
A55, A56, A57, A58, A59, A60, A61, A62, A63, A64, A65,
A66, A67, A68, A69, A70, A71, A72, A73, A74, A75 }
public static void main(String[] args) {
EnumSet<Big> bigEnumSet = EnumSet.allOf(Big.class);
System.out.println(bigEnumSet);
}
} /* Output:
[A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15,
A16, A17, A18, A19, A20, A21, A22, A23, A24, A25, A26, A27, A28, A29,
A30, A31, A32, A33, A34, A35, A36, A37, A38, A39, A40, A41, A42, A43,
A44, A45, A46, A47, A48, A49, A50, A51, A52, A53, A54, A55, A56, A57,
A58, A59, A60, A61, A62, A63, A64, A65, A66, A67, A68, A69, A70, A71,
A72, A73, A74, A75]
*///:~
```
The EnumSet clearly has no problem with an enum that has more than 64 elements, so we may presume that it adds another long when necessary. Exercise 7:(3) Find the source code for EnumSet and explain how it works.
## Using EnumMap
An EnumMap is a specialized Map that requires that its keys be from a single enum. Because of the constraints on an enum, an EnumMap can be implemented internally as an array. Thus they are extremely fast, so you can freely use EnumMapsfor enum-based lookups. You can only call put( ) for keys that are in your enum, but other than that it’s like using an ordinary Map. Here’s an example that demonstrates the use of the Command design pattern. This pattern starts with an interface containing (typically) a single method, and creates multiple implementations with different behavior for that method. You install Command objects, and your program calls them when necessary:
```java
//: enumerated/EnumMaps.java
// Basics of EnumMaps.
package enumerated;
import java.util.*;
import static enumerated.AlarmPoints.*;
import static net.mindview.util.Print.*;
interface Command { void action(); }
public class EnumMaps {
```

<!--p762-->
Enumerated Types
```java
public static void main(String[] args) {
EnumMap<AlarmPoints,Command> em =
new EnumMap<AlarmPoints,Command>(AlarmPoints.class);
em.put(KITCHEN, new Command() {
public void action() { print("Kitchen fire!"); }
});
em.put(BATHROOM, new Command() {
public void action() { print("Bathroom alert!"); }
});
for(Map.Entry<AlarmPoints,Command> e : em.entrySet()) {
printnb(e.getKey() + ": ");
e.getValue().action();
}
try { // If there’s no value for a particular key:
em.get(UTILITY).action();
} catch(Exception e) {
print(e);
}
}
} /* Output:
BATHROOM: Bathroom alert!
KITCHEN: Kitchen fire!
java.lang.NullPointerException
*///:~
```
Just as with EnumSet, the order of elements in the EnumMap is determined by their order of definition in the enum. The last part of main( ) shows that there is always a key entry for each of the enums, but the value is null unless you have called put( ) for that key. One advantage of EnumMap over constant-specific methods (described next) is that an EnumMap allows you to change the value objects, whereas you’ll see that constant-specific methods are fixed at compile time. As you’ll see later in the chapter, EnumMaps can be used to perform multiple dispatching for situations where you have multiple types of enums interacting with each other. Constant-specific methods Java enumshave a very interesting feature that allows you to give each enum instance different behavior by creating methods for each one. To do this, you define one or more abstract methods as part of the enum, then define the methods for each enum instance. For example:

<!--p763-->
```java
//: enumerated/ConstantSpecificMethod.java
import java.util.*;
import java.text.*;
public enum ConstantSpecificMethod {
DATE_TIME {
String getInfo() {
return
DateFormat.getDateInstance().format(new Date());
}
},
CLASSPATH {
String getInfo() {
return System.getenv("CLASSPATH");
}
},
VERSION {
String getInfo() {
return System.getProperty("java.version");
}
};
abstract String getInfo();
public static void main(String[] args) {
for(ConstantSpecificMethod csm : values())
System.out.println(csm.getInfo());
}
} /* (Execute to see output) *///:~
```
You can look up and call methods via their associated enum instance. This is often called table-driven code (and note the similarity to the aforementioned Command pattern). In object-oriented programming, different behavior is associated with different classes. Because each instance of an enum can have its own behavior via constant-specific methods, this suggests that each instance is a distinct type. In the above example, each enum instance is being treated as the "base type" ConstantSpecificMethod but you get polymorphic behavior with the method call getInfo( ). However, you can only take the similarity so far. You cannot treat enum instances as class types:
```java
//: enumerated/NotClasses.java
// {Exec: javap -c LikeClasses}
import static net.mindview.util.Print.*;
enum LikeClasses {
WINKEN { void behavior() { print("Behavior1"); } },
BLINKEN { void behavior() { print("Behavior2"); } },
NOD { void behavior() { print("Behavior3"); } };
abstract void behavior();
}
public class NotClasses {
// void f1(LikeClasses.WINKEN instance) {} // Nope
} /* Output:
Compiled from "NotClasses.java"
abstract class LikeClasses extends java.lang.Enum{
public static final LikeClasses WINKEN;
public static final LikeClasses BLINKEN;
public static final LikeClasses NOD;
...
*///:~
```

<!--p764-->
In f1( ), you can see that the compiler doesn’t allow you to use an enum instance as a class type, which makes sense if you consider the code generated by the compiler—each enum element is a static final instance of LikeClasses. Also, because they are static, enum instances of inner enums do not behave like ordinary inner classes; you cannot access non-static fields or methods in the outer class. As a more interesting example, consider a car wash. Each customer is given a menu of choices for their wash, and each option performs a different action. A constant-specific method can be associated with each option, and an EnumSet can be used to hold the customer’s selections: Enumerated Types
```java
//: enumerated/CarWash.java
import java.util.*;
import static net.mindview.util.Print.*;
public class CarWash {
public enum Cycle {
UNDERBODY {
void action() { print("Spraying the underbody"); }
},
WHEELWASH {
void action() { print("Washing the wheels"); }
},
PREWASH {
void action() { print("Loosening the dirt"); }
},
BASIC {
void action() { print("The basic wash"); }
},
HOTWAX {
void action() { print("Applying hot wax"); }
},
RINSE {
void action() { print("Rinsing"); }
},
BLOWDRY {
void action() { print("Blowing dry"); }
};
abstract void action();
}
EnumSet<Cycle> cycles =
EnumSet.of(Cycle.BASIC, Cycle.RINSE);
public void add(Cycle cycle) { cycles.add(cycle); }
public void washCar() {
for(Cycle c : cycles)
c.action();
}
public String toString() { return cycles.toString(); }
public static void main(String[] args) {
CarWash wash = new CarWash();
print(wash);
wash.washCar();
// Order of addition is unimportant:
wash.add(Cycle.BLOWDRY);
wash.add(Cycle.BLOWDRY); // Duplicates ignored
wash.add(Cycle.RINSE);
wash.add(Cycle.HOTWAX);
print(wash);
wash.washCar();
}
} /* Output:
[BASIC, RINSE]
The basic wash
Rinsing
[BASIC, HOTWAX, RINSE, BLOWDRY]
The basic wash
Applying hot wax
Rinsing
Blowing dry
*///:~
```

<!--p765-->
The syntax for defining a constant-specific method is effectively that of an anonymous inner class, but more succinct. This example also shows more characteristics of EnumSets. Since it’s a set, it will only hold one of each item, so duplicate calls to add( ) with the same argument are ignored (this makes sense, since you can only flip a bit "on" once). Also, the order that you add enum instances is unimportant—the output order is determined by the declaration order of the enum. Is it possible to override constant-specific methods, instead of implementing an abstract method? Yes, as you can see here:
```java
//: enumerated/OverrideConstantSpecific.java
import static net.mindview.util.Print.*;
public enum OverrideConstantSpecific {
NUT, BOLT,
WASHER {
void f() { print("Overridden method"); }
};
void f() { print("default behavior"); }
public static void main(String[] args) {
for(OverrideConstantSpecific ocs : values()) {
printnb(ocs + ": ");
ocs.f();
}
}
} /* Output:
NUT: default behavior
BOLT: default behavior
WASHER: Overridden method
*///:~
```
Although enums do prevent certain types of code, in general you should experiment with them as if they were classes.
## Chain of Responsibility with enums
In the Chain of Responsibility design pattern, you create a number of different ways to solve a problem and chain them together. When a request occurs, it is passed along the chain until one of the solutions can handle the request. You can easily implement a simple Chain of Responsibility with constantspecific methods. Consider a model of a post office, which tries to deal with each piece of mail in the most general way possible, but has to keep trying until it ends up treating the mail as a dead letter. Each attempt can be thought of as a Strategy (another design pattern), and the entire list together is a Chain of Responsibility. We start by describing a piece of mail. All the different characteristics of interest can be expressed using enums. Because the Mail objects will be randomly generated, the easiest way to reduce the probability of (for example) a piece of mail being given a YES for GeneralDelivery is to create more non-YES instances, so the enum definitions look a little funny at first. Within Mail, you’ll see randomMail( ), which creates random pieces of test mail. The generator( ) method produces an Iterable object that uses randomMail( ) to produce a number of mail objects, one each time you call next( ) via the iterator. This construct allows the simple creation of a foreach loop by calling Mail.generator( ):
```java
//: enumerated/PostOffice.java
// Modeling a post office.
```

<!--p766-->
Enumerated Types

<!--p767-->
```java
import java.util.*;
import net.mindview.util.*;
import static net.mindview.util.Print.*;
class Mail {
// The NO’s lower the probability of random selection:
enum GeneralDelivery {YES,NO1,NO2,NO3,NO4,NO5}
enum Scannability {UNSCANNABLE,YES1,YES2,YES3,YES4}
enum Readability {ILLEGIBLE,YES1,YES2,YES3,YES4}
enum Address {INCORRECT,OK1,OK2,OK3,OK4,OK5,OK6}
enum ReturnAddress {MISSING,OK1,OK2,OK3,OK4,OK5}
GeneralDelivery generalDelivery;
Scannability scannability;
Readability readability;
Address address;
ReturnAddress returnAddress;
static long counter = 0;
long id = counter++;
public String toString() { return "Mail " + id; }
public String details() {
return toString() +
", General Delivery: " + generalDelivery +
", Address Scanability: " + scannability +
", Address Readability: " + readability +
", Address Address: " + address +
", Return address: " + returnAddress;
}
// Generate test Mail:
public static Mail randomMail() {
Mail m = new Mail();
m.generalDelivery= Enums.random(GeneralDelivery.class);
m.scannability = Enums.random(Scannability.class);
m.readability = Enums.random(Readability.class);
m.address = Enums.random(Address.class);
m.returnAddress = Enums.random(ReturnAddress.class);
return m;
}
public static Iterable<Mail> generator(final int count) {
return new Iterable<Mail>() {
int n = count;
public Iterator<Mail> iterator() {
return new Iterator<Mail>() {
public boolean hasNext() { return n-- > 0; }
public Mail next() { return randomMail(); }
public void remove() { // Not implemented
throw new UnsupportedOperationException();
}
};
}
};
}
}
public class PostOffice {
enum MailHandler {
GENERAL_DELIVERY {
boolean handle(Mail m) {
switch(m.generalDelivery) {
case YES:
print("Using general delivery for " + m);
return true;
default: return false;
}
}
},
MACHINE_SCAN {
boolean handle(Mail m) {
switch(m.scannability) {
case UNSCANNABLE: return false;
default:
switch(m.address) {
case INCORRECT: return false;
default:
print("Delivering "+ m + " automatically");
return true;
}
}
}
},
VISUAL_INSPECTION {
boolean handle(Mail m) {
switch(m.readability) {
case ILLEGIBLE: return false;
default:
switch(m.address) {
case INCORRECT: return false;
default:
print("Delivering " + m + " normally");
return true;
}
}
}
},
RETURN_TO_SENDER {
boolean handle(Mail m) {
switch(m.returnAddress) {
case MISSING: return false;
default:
print("Returning " + m + " to sender");
return true;
}
}
};
abstract boolean handle(Mail m);
}
static void handle(Mail m) {
for(MailHandler handler : MailHandler.values())
if(handler.handle(m))
return;
print(m + " is a dead letter");
}
public static void main(String[] args) {
for(Mail mail : Mail.generator(10)) {
print(mail.details());
handle(mail);
print("*****");
}
}
} /* Output:
Mail 0, General Delivery: NO2, Address Scanability: UNSCANNABLE, Address
Readability: YES3, Address Address: OK1, Return address: OK1
Delivering Mail 0 normally
*****
Mail 1, General Delivery: NO5, Address Scanability: YES3, Address
Readability: ILLEGIBLE, Address Address: OK5, Return address: OK1
Delivering Mail 1 automatically
```

<!--p768-->
Enumerated Types
```java
*****
Mail 2, General Delivery: YES, Address Scanability: YES3, Address
Readability: YES1, Address Address: OK1, Return address: OK5
Using general delivery for Mail 2
*****
Mail 3, General Delivery: NO4, Address Scanability: YES3, Address
Readability: YES1, Address Address: INCORRECT, Return address: OK4
Returning Mail 3 to sender
*****
Mail 4, General Delivery: NO4, Address Scanability: UNSCANNABLE, Address
Readability: YES1, Address Address: INCORRECT, Return address: OK2
Returning Mail 4 to sender
*****
Mail 5, General Delivery: NO3, Address Scanability: YES1, Address
Readability: ILLEGIBLE, Address Address: OK4, Return address: OK2
Delivering Mail 5 automatically
*****
Mail 6, General Delivery: YES, Address Scanability: YES4, Address
Readability: ILLEGIBLE, Address Address: OK4, Return address: OK4
Using general delivery for Mail 6
*****
Mail 7, General Delivery: YES, Address Scanability: YES3, Address
Readability: YES4, Address Address: OK2, Return address: MISSING
Using general delivery for Mail 7
*****
Mail 8, General Delivery: NO3, Address Scanability: YES1, Address
Readability: YES3, Address Address: INCORRECT, Return address: MISSING
Mail 8 is a dead letter
*****
Mail 9, General Delivery: NO1, Address Scanability: UNSCANNABLE, Address
Readability: YES2, Address Address: OK1, Return address: OK4
Delivering Mail 9 normally
*****
*///:~
```
The Chain of Responsibility is expressed in enum MailHandler, and the order of the enum definitions determines the order in which the strategies are attempted on each piece of mail. Each strategy is tried in turn until one succeeds or they all fail, in which case you have a dead letter. Exercise 8:(6) Modify PostOffice.java so it has the ability to forward mail. Exercise 9:(5) Modify class PostOffice so that it uses an EnumMap. Project:2 Specialized languages like Prolog use backward chaining in order to solve problems like this. Using PostOffice.java for inspiration, research such languages and develop a program that allows new "rules" to be easily added to the system.
## State machines with enums

<!--p769-->
Enumerated types can be ideal for creating state machines. A state machine can be in a finite number of specific states. The machine normally moves from one state to the next based on an input, but there are also transient states; the machine moves out of these as soon as their task is performed. 2 Projects are suggestions to be used (for example) as term projects. Solutions to projects are not included in the solution guide. There are certain allowable inputs for each state, and different inputs change the state of the machine to different new states. Because enumsrestrict the set of possible cases, they are quite useful for enumerating the different states and inputs. Each state also typically has some kind of associated output. A vending machine is a good example of a state machine. First, we define the various inputs in an enum:
```java
//: enumerated/Input.java
package enumerated;
import java.util.*;
public enum Input {
NICKEL(5), DIME(10), QUARTER(25), DOLLAR(100),
TOOTHPASTE(200), CHIPS(75), SODA(100), SOAP(50),
ABORT_TRANSACTION {
public int amount() { // Disallow
throw new RuntimeException("ABORT.amount()");
}
},
STOP { // This must be the last instance.
public int amount() { // Disallow
throw new RuntimeException("SHUT_DOWN.amount()");
}
};
int value; // In cents
Input(int value) { this.value = value; }
Input() {}
int amount() { return value; }; // In cents
static Random rand = new Random(47);
public static Input randomSelection() {
// Don’t include STOP:
return values()[rand.nextInt(values().length - 1)];
}
} ///:~
```
Note that two of the Inputshave an associated amount, so amount( ) is defined in the interface. However, it is inappropriate to call amount( ) for the other two Input types, so they throw an exception if you call amount( ). Although this is a bit of an odd setup (define a method in an interface, then throw an exception if you call it for certain implementations), it is imposed upon us because of the constraints of enums. The VendingMachine will react to these inputs by first categorizing them via the Category enum, so that it can switch on the categories. This example shows how enums make code clearer and easier to manage:
```java
//: enumerated/VendingMachine.java
// {Args: VendingMachineInput.txt}
package enumerated;
import java.util.*;
import net.mindview.util.*;
import static enumerated.Input.*;
import static net.mindview.util.Print.*;
enum Category {
MONEY(NICKEL, DIME, QUARTER, DOLLAR),
ITEM_SELECTION(TOOTHPASTE, CHIPS, SODA, SOAP),
QUIT_TRANSACTION(ABORT_TRANSACTION),
SHUT_DOWN(STOP);
private Input[] values;
```

<!--p770-->
Enumerated Types

<!--p771-->
```java
Category(Input... types) { values = types; }
private static EnumMap<Input,Category> categories =
new EnumMap<Input,Category>(Input.class);
static {
for(Category c : Category.class.getEnumConstants())
for(Input type : c.values)
categories.put(type, c);
}
public static Category categorize(Input input) {
return categories.get(input);
}
}
public class VendingMachine {
private static State state = State.RESTING;
private static int amount = 0;
private static Input selection = null;
enum StateDuration { TRANSIENT } // Tagging enum
enum State {
RESTING {
void next(Input input) {
switch(Category.categorize(input)) {
case MONEY:
amount += input.amount();
state = ADDING_MONEY;
break;
case SHUT_DOWN:
state = TERMINAL;
default:
}
}
},
ADDING_MONEY {
void next(Input input) {
switch(Category.categorize(input)) {
case MONEY:
amount += input.amount();
break;
case ITEM_SELECTION:
selection = input;
if(amount < selection.amount())
print("Insufficient money for " + selection);
else state = DISPENSING;
break;
case QUIT_TRANSACTION:
state = GIVING_CHANGE;
break;
case SHUT_DOWN:
state = TERMINAL;
default:
}
}
},
DISPENSING(StateDuration.TRANSIENT) {
void next() {
print("here is your " + selection);
amount -= selection.amount();
state = GIVING_CHANGE;
}
},
GIVING_CHANGE(StateDuration.TRANSIENT) {
void next() {
if(amount > 0) {
print("Your change: " + amount);
amount = 0;
}
state = RESTING;
}
},
TERMINAL { void output() { print("Halted"); } };
private boolean isTransient = false;
State() {}
State(StateDuration trans) { isTransient = true; }
void next(Input input) {
throw new RuntimeException("Only call " +
"next(Input input) for non-transient states");
}
void next() {
throw new RuntimeException("Only call next() for " +
"StateDuration.TRANSIENT states");
}
void output() { print(amount); }
}
static void run(Generator<Input> gen) {
while(state != State.TERMINAL) {
state.next(gen.next());
while(state.isTransient)
state.next();
state.output();
}
}
public static void main(String[] args) {
Generator<Input> gen = new RandomInputGenerator();
if(args.length == 1)
gen = new FileInputGenerator(args[0]);
run(gen);
}
}
// For a basic sanity check:
class RandomInputGenerator implements Generator<Input> {
public Input next() { return Input.randomSelection(); }
}
// Create Inputs from a file of ‘;’-separated strings:
class FileInputGenerator implements Generator<Input> {
private Iterator<String> input;
public FileInputGenerator(String fileName) {
input = new TextFile(fileName, ";").iterator();
}
public Input next() {
if(!input.hasNext())
return null;
return Enum.valueOf(Input.class, input.next().trim());
}
} /* Output:
here is your CHIPS
here is your TOOTHPASTE
```

<!--p772-->
Enumerated Types
```java
Your change: 35
Insufficient money for SODA
Insufficient money for SODA
Your change: 75
Halted
*///:~
```
Because selecting among enum instances is most often accomplished with a switch statement (notice the extra effort that the language goes to in order to make a switch on enumseasy), one of the most common questions to ask when you are organizing multiple enums is "What do I want to switch on?" Here, it’s easiest to work back from the VendingMachine by noting that in each State, you need to switch on the basic categories of input action: money being inserted, an item being selected, the transaction being aborted, and the machine being turned off. However, within those categories, you have different types of money that can be inserted and different items that can be selected. The Category enum groups the different types of Input so that the categorize( ) method can produce the appropriate Category inside a switch. This method uses an EnumMap to efficiently and safely perform the lookup. If you study class VendingMachine, you can see how each state is different, and responds differently to input. Also note the two transient states; in run( ) the machine waits for an Input and doesn’t stop moving through states until it is no longer in a transient state. The VendingMachine can be tested in two ways, by using two different Generator objects. The RandomInputGenerator just keeps producing inputs, everything except SHUT_DOWN. By running this for a long time you get a kind of sanity check to help ensure that the machine will not wander into a bad state. The FilelnputGenerator takes a file describing inputs in text form, turns them into enum instances, and creates Input objects. Here’s the text file used to produce the output shown above:
```java
QUARTER; QUARTER; QUARTER; CHIPS;
DOLLAR; DOLLAR; TOOTHPASTE;
QUARTER; DIME; ABORT_TRANSACTION;
QUARTER; DIME; SODA;
QUARTER; DIME; NICKEL; SODA;
ABORT_TRANSACTION;
STOP;
///:~
```

<!--p773-->
One limitation to this design is that the fields in VendingMachine that are accessed by enum State instances must be static, which means you can only have a single VendingMachine instance. This may not be that big of an issue if you think about an actual (embedded Java) implementation, since you are likely to have only one application per machine. Exercise 10:(7) Modify class VendingMachine (only) using EnumMap so that one program can have multiple instances of VendingMachine. Enumerated Types Exercise 11:(7) In a real vending machine you will want to easily add and change the type of vended items, so the limits imposed by an enum on Input are impractical (remember that enums are for a restricted set of types). Modify VendingMachine.java so that the vended items are represented by a class instead of being part of Input, and initialize an Array List of these objects from a text file (using net.mindview.util.TextFile). Project3Design the vending machine using internationalization, so that one machine can easily be adapted to all countries. Multiple dispatching When you are dealing with multiple interacting types, a program can get particularly messy. For example, consider a system that parses and executes mathematical expressions. You want to say Number.plus(Number), Number.multiply(Number), etc., where Number is the base class for a family of numerical objects. But when you say a.plus(b), and you don’t know the exact type of either a or b, how can you get them to interact properly? The answer starts with something you probably don’t think about: Java only performs single dispatching. That is, if you are performing an operation on more than one object whose type is unknown, Java can invoke the dynamic binding mechanism on only one of those types. This doesn’t solve the problem described here, so you end up detecting some types manually and effectively producing your own dynamic binding behavior. The solution is called multiple dispatching. (In this case, there will be only two dispatches, which is referred to as double dispatching.) Polymorphism can only occur via method calls, so if you want double dispatching, there must be two method calls: the first to determine the first unknown type, and the second to determine the second unknown type. With multiple dispatching, you must have a virtual call for each of the types—if you are working with two different type hierarchies that are interacting, you’ll need a virtual call in each hierarchy. Generally, you’ll set up a configuration such that a single method call produces more than one virtual method call and thus services more than one type in the process. To get this effect, you need to work with more than one method: You’ll need a method call for each dispatch. The methods in the following example (which implements the "paper, scissors, rock" game, traditionally called RoShamBo) are called compete( ) and eval( ) and are both members of the same type. They produce one of three possible outcomes:4
```java
//: enumerated/Outcome.java
package enumerated;
public enum Outcome { WIN, LOSE, DRAW } ///:~
//: enumerated/RoShamBo1.java
// Demonstration of multiple dispatching.
package enumerated;
import java.util.*;
import static enumerated.Outcome.*;
interface Item {
Outcome compete(Item it);
Outcome eval(Paper p);
Outcome eval(Scissors s);
Outcome eval(Rock r);
```

<!--p774-->
3 Projects are suggestions to be used (for example) as term projects. Solutions to projects are not included in the solution guide. 4 This example existed for a number of years in both C++ and Java (in Thinking in Patterns) on www.MindView.net before it appeared, without attribution, in a book by other authors.

<!--p775-->
```java
}
class Paper implements Item {
public Outcome compete(Item it) { return it.eval(this); }
public Outcome eval(Paper p) { return DRAW; }
public Outcome eval(Scissors s) { return WIN; }
public Outcome eval(Rock r) { return LOSE; }
public String toString() { return "Paper"; }
}
class Scissors implements Item {
public Outcome compete(Item it) { return it.eval(this); }
public Outcome eval(Paper p) { return LOSE; }
public Outcome eval(Scissors s) { return DRAW; }
public Outcome eval(Rock r) { return WIN; }
public String toString() { return "Scissors"; }
}
class Rock implements Item {
public Outcome compete(Item it) { return it.eval(this); }
public Outcome eval(Paper p) { return WIN; }
public Outcome eval(Scissors s) { return LOSE; }
public Outcome eval(Rock r) { return DRAW; }
public String toString() { return "Rock"; }
}
public class RoShamBo1 {
static final int SIZE = 20;
private static Random rand = new Random(47);
public static Item newItem() {
switch(rand.nextInt(3)) {
default:
case 0: return new Scissors();
case 1: return new Paper();
case 2: return new Rock();
}
}
public static void match(Item a, Item b) {
System.out.println(
a + " vs. " + b + ": " + a.compete(b));
}
public static void main(String[] args) {
for(int i = 0; i < SIZE; i++)
match(newItem(), newItem());
}
} /* Output:
Rock vs. Rock: DRAW
Paper vs. Rock: WIN
Paper vs. Rock: WIN
Paper vs. Rock: WIN
Scissors vs. Paper: WIN
Scissors vs. Scissors: DRAW
Scissors vs. Paper: WIN
Rock vs. Paper: LOSE
Paper vs. Paper: DRAW
Rock vs. Paper: LOSE
Paper vs. Scissors: LOSE
Paper vs. Scissors: LOSE
Rock vs. Scissors: WIN
Rock vs. Paper: LOSE
Paper vs. Rock: WIN
Scissors vs. Paper: WIN
Paper vs. Scissors: LOSE
Paper vs. Scissors: LOSE
Paper vs. Scissors: LOSE
Paper vs. Scissors: LOSE
*///:~
```
Item is the interface for the types that will be multiply dispatched. RoShamBo1.match( ) takes two Item objects and begins the doubledispatching process by calling the Item.compete( ) function. The virtual mechanism determines the type of a, so it wakes up inside the compete( ) function of a’s concrete type. The compete( ) function performs the second dispatch by calling eval( ) on the remaining type. Passing itself (this)as an argument to eval( ) produces a call to the overloaded eval( ) function, thus preserving the type information of the first dispatch. When the second dispatch is completed, you know the exact types of both Item objects. It requires a lot of ceremony to set up multiple dispatching, but keep in mind that the benefit is the syntactic elegance achieved when making the callinstead of writing awkward code to determine the type of one or more objects during a call, you simply say, "You two! I don’t care what types you are, interact properly with each other!" Make sure this kind of elegance is important to you before embarking on multiple dispatching, however.
## Dispatching with enums
Performing a straight translation of RoShamBo1.java into an enum-based solution is problematic because enum instances are not types, so the overloaded eval( ) methods won’t work—you can’t use enum instances as argument types. However, there are a number of different approaches to implementing multiple dispatching which benefit from enums. One approach uses a constructor to initialize each e n um instance with a "row" of outcomes; taken together this produces a kind of lookup table:
```java
//: enumerated/RoShamBo2.java
// Switching one enum on another.
package enumerated;
import static enumerated.Outcome.*;
public enum RoShamBo2 implements Competitor<RoShamBo2> {
PAPER(DRAW, LOSE, WIN),
SCISSORS(WIN, DRAW, LOSE),
ROCK(LOSE, WIN, DRAW);
private Outcome vPAPER, vSCISSORS, vROCK;
RoShamBo2(Outcome paper,Outcome scissors,Outcome rock) {
this.vPAPER = paper;
this.vSCISSORS = scissors;
this.vROCK = rock;
}
public Outcome compete(RoShamBo2 it) {
switch(it) {
default:
case PAPER: return vPAPER;
case SCISSORS: return vSCISSORS;
case ROCK: return vROCK;
}
}
public static void main(String[] args) {
RoShamBo.play(RoShamBo2.class, 20);
}
} /* Output:
ROCK vs. ROCK: DRAW
SCISSORS vs. ROCK: LOSE
SCISSORS vs. ROCK: LOSE
```

<!--p776-->
Enumerated Types
```java
SCISSORS vs. ROCK: LOSE
PAPER vs. SCISSORS: LOSE
PAPER vs. PAPER: DRAW
PAPER vs. SCISSORS: LOSE
ROCK vs. SCISSORS: WIN
SCISSORS vs. SCISSORS: DRAW
ROCK vs. SCISSORS: WIN
SCISSORS vs. PAPER: WIN
SCISSORS vs. PAPER: WIN
ROCK vs. PAPER: LOSE
ROCK vs. SCISSORS: WIN
SCISSORS vs. ROCK: LOSE
PAPER vs. SCISSORS: LOSE
SCISSORS vs. PAPER: WIN
SCISSORS vs. PAPER: WIN
SCISSORS vs. PAPER: WIN
SCISSORS vs. PAPER: WIN
*///:~
```
Once both types have been determined in compete( ), the only action is the return of the resulting Outcome. However, you could also call another method, even (for example) via a Command object that was assigned in the constructor. RoShamBo2.java is much smaller and more straightforward than the original example, and thus easier to keep track of. Notice that you’re still using two dispatches to determine the type of both objects. In RoShamBo1.java, both dispatches were performed using virtual method calls, but here, only the first dispatch uses a virtual method call. The second dispatch uses a switch, but is safe because the enum limits the choices in the switch statement. The code that drives the enum has been separated out so that it can be used in the other examples. First, the Competitor interface defines a type that competes with another Competitor:
```java
//: enumerated/Competitor.java
// Switching one enum on another.
package enumerated;
public interface Competitor<T extends Competitor<T>> {
Outcome compete(T competitor);
} ///:~
```
Then we define two static methods (static to avoid having to specify the parameter type explicitly). First, match( ) calls compete( ) for one Competitor vs. another, and you can see that in this case the type parameter only needs to be a Competitor<T>. But in play( ), the type parameter must be both an Enum<T> because it is used in Enums.random( ), and a Competitor<T> because it is passed to match( ):

<!--p777-->
```java
//: enumerated/RoShamBo.java
// Common tools for RoShamBo examples.
package enumerated;
import net.mindview.util.*;
public class RoShamBo {
public static <T extends Competitor<T>>
void match(T a, T b) {
System.out.println(
a + " vs. " + b + ": " + a.compete(b));
}
public static <T extends Enum<T> & Competitor<T>>
void play(Class<T> rsbClass, int size) {
for(int i = 0; i < size; i++)
match(
Enums.random(rsbClass),Enums.random(rsbClass));
}
} ///:~
```
The play( ) method does not have a return value that involves the type parameter T, so it seems like you might use wildcards inside the Class<T> type instead of using the leading parameter description. However, wildcards cannot extend more than one base type, so we must use the above expression. Using constant-specific methods Because constant-specific methods allow you to provide different method implementations for each enum instance, they might seem like a perfect solution for setting up multiple dispatching. But even though they can be given different behavior in this way, enum instances are not types, so you cannot use them as argument types in method signatures. The best you can do for this example is to set up a switch statement:
```java
//: enumerated/RoShamBo3.java
// Using constant-specific methods.
package enumerated;
import static enumerated.Outcome.*;
public enum RoShamBo3 implements Competitor<RoShamBo3> {
PAPER {
public Outcome compete(RoShamBo3 it) {
switch(it) {
default: // To placate the compiler
case PAPER: return DRAW;
case SCISSORS: return LOSE;
case ROCK: return WIN;
}
}
},
SCISSORS {
public Outcome compete(RoShamBo3 it) {
switch(it) {
default:
case PAPER: return WIN;
case SCISSORS: return DRAW;
case ROCK: return LOSE;
}
}
},
ROCK {
public Outcome compete(RoShamBo3 it) {
switch(it) {
default:
case PAPER: return LOSE;
case SCISSORS: return WIN;
case ROCK: return DRAW;
}
}
};
public abstract Outcome compete(RoShamBo3 it);
public static void main(String[] args) {
RoShamBo.play(RoShamBo3.class, 20);
}
} /* Same output as RoShamBo2.java *///:~
```

<!--p778-->
Enumerated Types Although this is functional and not unreasonable, the solution of RoShamBo2.java seems to require less code when adding a new type, and thus seems more straightforward. However, RoShamBo3.java can be simplified and compressed:
```java
//: enumerated/RoShamBo4.java
package enumerated;
public enum RoShamBo4 implements Competitor<RoShamBo4> {
ROCK {
public Outcome compete(RoShamBo4 opponent) {
return compete(SCISSORS, opponent);
}
},
SCISSORS {
public Outcome compete(RoShamBo4 opponent) {
return compete(PAPER, opponent);
}
},
PAPER {
public Outcome compete(RoShamBo4 opponent) {
return compete(ROCK, opponent);
}
};
Outcome compete(RoShamBo4 loser, RoShamBo4 opponent) {
return ((opponent == this) ? Outcome.DRAW
: ((opponent == loser) ? Outcome.WIN
: Outcome.LOSE));
}
public static void main(String[] args) {
RoShamBo.play(RoShamBo4.class, 20);
}
} /* Same output as RoShamBo2.java *///:~
```
Here, the second dispatch is performed by the two-argument version of compete( ), which performs a sequence of comparisons and is thus similar to the action of a switch. It’s smaller, but a bit confusing. For a large system this confusion can become debilitating.
## Dispatching with EnumMaps
It’s possible to perform a "true" double dispatch using the EnumMap class, which is specifically designed to work very efficiently with enums. Since the goal is to switch on two unknown types, an EnumMap of EnumMapscan be used to produce the double dispatch:

<!--p779-->
```java
//: enumerated/RoShamBo5.java
// Multiple dispatching using an EnumMap of EnumMaps.
package enumerated;
import java.util.*;
import static enumerated.Outcome.*;
enum RoShamBo5 implements Competitor<RoShamBo5> {
PAPER, SCISSORS, ROCK;
static EnumMap<RoShamBo5,EnumMap<RoShamBo5,Outcome>>
table = new EnumMap<RoShamBo5,
EnumMap<RoShamBo5,Outcome>>(RoShamBo5.class);
static {
for(RoShamBo5 it : RoShamBo5.values())
table.put(it,
new EnumMap<RoShamBo5,Outcome>(RoShamBo5.class));
initRow(PAPER, DRAW, LOSE, WIN);
initRow(SCISSORS, WIN, DRAW, LOSE);
initRow(ROCK, LOSE, WIN, DRAW);
}
static void initRow(RoShamBo5 it,
Outcome vPAPER, Outcome vSCISSORS, Outcome vROCK) {
EnumMap<RoShamBo5,Outcome> row =
RoShamBo5.table.get(it);
row.put(RoShamBo5.PAPER, vPAPER);
row.put(RoShamBo5.SCISSORS, vSCISSORS);
row.put(RoShamBo5.ROCK, vROCK);
}
public Outcome compete(RoShamBo5 it) {
return table.get(this).get(it);
}
public static void main(String[] args) {
RoShamBo.play(RoShamBo5.class, 20);
}
} /* Same output as RoShamBo2.java *///:~
```
The EnumMap is initialized using a static clause; you can see the table-like structure of the calls to initRow( ). Notice the compete( ) method, where you can see both dispatches happening in a single statement. Using a 2-D array We can simplify the solution even more by noting that each enum instance has a fixed value (based on its declaration order) and that ordinal( ) produces this value. A two-dimensional array mapping the competitors onto the outcomes produces the smallest and most straightforward solution (and possibly the fastest, although remember that EnumMap uses an internal array):
```java
//: enumerated/RoShamBo6.java
// Enums using "tables" instead of multiple dispatch.
package enumerated;
import static enumerated.Outcome.*;
enum RoShamBo6 implements Competitor<RoShamBo6> {
PAPER, SCISSORS, ROCK;
private static Outcome[][] table = {
{ DRAW, LOSE, WIN }, // PAPER
{ WIN, DRAW, LOSE }, // SCISSORS
{ LOSE, WIN, DRAW }, // ROCK
};
public Outcome compete(RoShamBo6 other) {
return table[this.ordinal()][other.ordinal()];
}
public static void main(String[] args) {
RoShamBo.play(RoShamBo6.class, 20);
}
} ///:~
```

<!--p780-->

<!--p781-->
The table has exactly the same order as the calls to initRow( ) in the previous example. The small size of this code holds great appeal over the previous examples, partly because it seems much easier to understand and modify but also because it just seems more straightforward. However, it’s not quite as "safe" as the previous examples because it uses an array. With a larger array, you might get the size wrong, and if your tests do not cover all possibilities something could slip through the cracks. Enumerated Types All of these solutions are different types of tables, but it’s worth exploring the expression of the tables to find the one that fits best. Note that even though the above solution is the most compact, it is also fairly rigid because it can only produce a constant output given constant inputs. However, there’s nothing that prevents you from having table produce a function object. For certain types of problems, the concept of "table-driven code" can be very powerful. Enumerated Types Summary Even though enumerated types are not terribly complex in themselves, this chapter was postponed until later in the book because of what you can do with enumsin combination with features like polymorphism, generics, and reflection. Although they are significantly more sophisticated than enumsin C or C++, enumsare still a "small" feature, something the language has survived (a bit awkwardly) without for many years. And yet this chapter shows the valuable impact that a "small" feature can have— sometimes it gives you just the right leverage to solve a problem elegantly and clearly, and as I have been saying throughout this book, elegance is important, and clarity may make the difference between a successful solution and one that fails because others cannot understand it. On the subject of clarity, an unfortunate source of confusion comes from the poor choice in Java 1.0 of the term "enumeration" instead of the common and well-accepted term "iterator" to indicate an object that selects each element of a sequence (as shown in Collections). Some languages even refer to enumerated data types as "enumerators!" This mistake has since been rectified in Java, but the Enumeration interface could not, of course, simply be removed and so is still hanging around in old (and sometimes new!) code, the library, and documentation. Solutions to selected exercises can be found in the electronic document The Thinking in Java Annotated Solution Guide, available for sale from www.MindView.net.