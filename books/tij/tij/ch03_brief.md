# 3. Operators (printed p63-92)


<!--p85-->
```java
System.out.println("Rather a lot to type");
```
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
```java
a = 4;
```
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
```java
t1.level = t2.level;
```
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
```java
y.c = ‘z’;
```

<!--p89-->
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
```java
x = -a;
```
```java
x = a * -b;
```
```java
x = a * (-b);
```
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
```java
test1(0) && test2(2) && test3(2)
```
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
```java
long n3 = 200;
```
```java
float f4 = 1e-43f; // 10 to the power
```

<!--p98-->

<!--p99-->
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
```java
boolean-exp ? value0 : value1
```
```java
//: operators/TernaryIfElse.java
```

<!--p102-->
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
```java
while(x = y) {
// ....
}
```

<!--p104-->
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

<!--p113-->
```java
//: operators/Overflow.java
// Surprise! Java lets you overflow.
public class Overflow {
public static void main(String[] args) {
```
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