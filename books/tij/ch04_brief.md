# 4. Controlling Execution (printed p93-106)


<!--p115-->
Controlling Execution Like a sentient creature, a program must manipulate its world and make choices during execution. In Java you make choices with execution control statements. Java uses all of C’s execution control statements, so if you’ve programmed with C or C++, then most of what you see will be familiar. Most procedural programming languages have some kind of control statements, and there is often overlap among languages. In Java, the keywords include if-else, while, do-while, for, return, break, and a selection statement called switch. Java does not, however, support the much-maligned goto (which can still be the most expedient way to solve certain types of problems). You can still do a goto-like jump, but it is much more constrained than a typical goto.
## true and false
All conditional statements use the truth or falsehood of a conditional expression to determine the execution path. An example of a conditional expression is a == b. This uses the conditional operator == to see if the value of a is equivalent to the value of b. The expression returns true or false. Any of the relational operators you’ve seen in the previous chapter can be used to produce a conditional statement. Note that Java doesn’t allow you to use a number as a boolean, even though it’s allowed in C and C++ (where truth is nonzero and falsehood is zero). If you want to use a non-boolean in a boolean test, such as if(a), you must first convert it to a boolean value by using a conditional expression, such as if(a != 0).
## if-else
The if-else statement is the most basic way to control program flow. The else is optional, so you can use if in two forms:
```java
if(Boolean-expression)
statement
```
or
```java
if(Boolean-expression)
statement
else
statement
```
The Boolean-expression must produce a boolean result. The statement is either a simple statement terminated by a semicolon, or a compound statement, which is a group of simple statements enclosed in braces. Whenever the word “statement” is used, it always implies that the statement can be simple or compound. As an example of if-else, here is a test( ) method that will tell you whether a guess is above, below, or equivalent to a target number:

<!--p116-->
```java
//: control/IfElse.java
import static net.mindview.util.Print.*;
public class IfElse {
static int result = 0;
static void test(int testval, int target) {
if(testval > target)
result = +1;
else if(testval < target)
result = -1;
else
result = 0; // Match
}
public static void main(String[] args) {
test(10, 5);
print(result);
test(5, 10);
print(result);
test(5, 5);
print(result);
}
} /* Output:
-1
*///:~
```
In the middle of test( ), you’ll also see an “else if,” which is not a new keyword but just an else followed by a new if statement. Although Java, like C and C++ before it, is a “free-form” language, it is conventional to indent the body of a control flow statement so the reader can easily determine where it begins and ends. Iteration Looping is controlled by while, do-while and for, which are sometimes classified as iteration statements. A statement repeats until the controlling Boolean-expression evaluates to false. The form for a while loop is:
```java
while(Boolean-expression)
statement
```
The Boolean-expression is evaluated once at the beginning of the loop and again before each further iteration of the statement. Here’s a simple example that generates random numbers until a particular condition is met:

<!--p117-->
```java
//: control/WhileTest.java
// Demonstrates the while loop.
public class WhileTest {
static boolean condition() {
boolean result = Math.random() < 0.99;
System.out.print(result + ", ");
return result;
}
public static void main(String[] args) {
while(condition())
System.out.println("Inside ‘while’");
System.out.println("Exited ‘while’");
}
} /* (Execute to see output) *///:~
```
The condition( ) method uses the static method random( ) in the Math library, which generates a double value between 0 and 1. (It includes 0, but not 1.) The result value comes from the comparison operator <, which produces a boolean result. If you print a boolean value, you automatically get the appropriate string “true” or “false.” The conditional expression for the while says: “repeat the statements in the body as long as condition( ) returns true.”
## do-while
The form for do-while is
```java
do
statement
while(Boolean-expression);
```
The sole difference between while and do-while is that the statement of the do-while always executes at least once, even if the expression evaluates to false the first time. In a while, if the conditional is false the first time the statement never executes. In practice, do- while is less common than while.
## for
A for loop is perhaps the most commonly used form of iteration. This loop performs initialization before the first iteration. Then it performs conditional testing and, at the end of each iteration, some form of “stepping.” The form of the for loop is:
```java
for(initialization; Boolean-expression; step)
statement
```
Any of the expressions initialization, Boolean-expression or step can be empty. The expression is tested before each iteration, and as soon as it evaluates to false, execution will continue at the line following the for statement. At the end of each loop, the step executes. for loops are usually used for “counting” tasks:
```java
//: control/ListCharacters.java
// Demonstrates "for" loop by listing
// all the lowercase ASCII letters.
public class ListCharacters {
public static void main(String[] args) {
for(char c = 0; c < 128; c++)
if(Character.isLowerCase(c))
System.out.println("value: " + (int)c +
" character: " + c);
}
} /* Output:
value: 97 character: a
value: 98 character: b
value: 99 character: c
value: 100 character: d
value: 101 character: e
value: 102 character: f
value: 103 character: g
value: 104 character: h
value: 105 character: i
value: 106 character: j
...
```

<!--p118-->
Controlling Execution
```java
*///:~
```
Note that the variable c is defined at the point where it is used, inside the control expression of the for loop, rather than at the beginning of main( ). The scope of c is the statement controlled by the for. This program also uses the java.lang.Character “wrapper” class, which not only wraps the primitive char type in an object, but also provides other utilities. Here, the static isLowerCase( ) method is used to detect whether the character in question is a lowercase letter. Traditional procedural languages like C require that all variables be defined at the beginning of a block so that when the compiler creates a block, it can allocate space for those variables. In Java and C++, you can spread your variable declarations throughout the block, defining them at the point that you need them. This allows a more natural coding style and makes code easier to understand. Exercise 1:(1) Write a program that prints values from 1 to 100. Exercise 2:(2) Write a program that generates 25 random int values. For each value, use an if-else statement to classify it as greater than, less than, or equal to a second randomly generated value. Exercise 3:(1) Modify Exercise 2 so that your code is surrounded by an “infinite” while loop. It will then run until you interrupt it from the keyboard (typically by pressing Control- C). Exercise 4: (3) Write a program that uses two nested for loops and the modulus operator (%) to detect and print prime numbers (integral numbers that are not evenly divisible by any other numbers except for themselves and 1). Exercise 5:(4) Repeat Exercise 10 from the previous chapter, using the ternary operator and a bitwise test to display the ones and zeroes, instead of Integer.toBinaryString( ). The comma operator Earlier in this chapter I stated that the comma operator (not the comma separator, which is used to separate definitions and method arguments) has only one use in Java: in the control expression of a for loop. In both the initialization and step portions of the control expression, you can have a number of statements separated by commas, and those statements will be evaluated sequentially. Using the comma operator, you can define multiple variables within a for statement, but they must be of the same type:

<!--p119-->
```java
//: control/CommaOperator.java
public class CommaOperator {
public static void main(String[] args) {
for(int i = 1, j = i + 10; i < 5; i++, j = i * 2) {
System.out.println("i = " + i + " j = " + j);
}
}
} /* Output:
i = 1 j = 11
i = 2 j = 4
i = 3 j = 6
i = 4 j = 8
*///:~
```
The int definition in the for statement covers both i and j. The initialization portion can have any number of definitions of one type. The ability to define variables in a control expression is limited to the for loop. You cannot use this approach with any of the other selection or iteration statements. You can see that in both the initialization and step portions, the statements are evaluated in sequential order. Foreach syntax Java SE5 introduces a new and more succinct for syntax, for use with arrays and containers (you’ll learn more about these in the Arrays and Containers in Depth chapter). This is often called the foreach syntax, and it means that you don’t have to create an int to count through a sequence of items—the foreach produces each item for you, automatically. For example, suppose you have an array of float and you’d like to select each element in that array:
```java
//: control/ForEachFloat.java
import java.util.*;
public class ForEachFloat {
public static void main(String[] args) {
Random rand = new Random(47);
float f[] = new float[10];
for(int i = 0; i < 10; i++)
f[i] = rand.nextFloat();
for(float x : f)
System.out.println(x);
}
} /* Output:
0.72711575
0.39982635
0.5309454
0.0534122
0.16020656
0.57799757
0.18847865
0.4170137
0.51660204
0.73734957
*///:~
```
The array is populated using the old for loop, because it must be accessed with an index. You can see the foreach syntax in the line:
```java
for(float x : f) {
```

<!--p120-->
This defines a variable x of type float and sequentially assigns each element of f to x. Any method that returns an array is a candidate for use with foreach. For example, the String class has a method toCharArray( ) that returns an array of char, so you can easily iterate through the characters in a string: Controlling Execution
```java
//: control/ForEachString.java
public class ForEachString {
public static void main(String[] args) {
for(char c : "An African Swallow".toCharArray() )
System.out.print(c + " ");
}
} /* Output:
A n A f r i c a n S w a l l o w
*///:~
```
As you’ll see in the Holding Your Objects chapter, foreach will also work with any object that is Iterable. Many for statements involve stepping through a sequence of integral values, like this:
```java
for(int i = 0; i < 100; i++)
```
For these, the foreach syntax won’t work unless you want to create an array of int first. To simplify this task, I’ve created a method called range( ) in net.mindview.util.Range that automatically generates the appropriate array. My intent is for range( ) to be used as a static import:
```java
//: control/ForEachInt.java
import static net.mindview.util.Range.*;
import static net.mindview.util.Print.*;
public class ForEachInt {
public static void main(String[] args) {
for(int i : range(10)) // 0..9
printnb(i + " ");
print();
for(int i : range(5, 10)) // 5..9
printnb(i + " ");
print();
for(int i : range(5, 20, 3)) // 5..20 step 3
printnb(i + " ");
print();
}
} /* Output:
0 1 2 3 4 5 6 7 8 9
5 6 7 8 9
5 8 11 14 17
*///:~
```

<!--p121-->
The range( ) method has been overloaded, which means the same method name can be used with different argument lists (you’ll learn about overloading soon). The first overloaded form of range( ) just starts at zero and produces values up to but not including the top end of the range. The second form starts at the first value and goes until one less than the second, and the third form has a step value so it increases by that value. range( ) is a very simple version of what’s called a generator, which you’ll see later in the book. Note that although range( ) allows the use of the foreach syntax in more places, and thus arguably increases readability, it is a little less efficient, so if you are tuning for performance you may want to use a profiler, which is a tool that measures the performance of your code. You’ll note the use of printnb( ) in addition to print( ). The printnb( ) method does not emit a newline, so it allows you to output a line in pieces. The foreach syntax not only saves time when typing in code. More importantly, it is far easier to read and says what you are trying to do (get each element of the array) rather than giving the details of how you are doing it (“I’m creating this index so I can use it to select each of the array elements.”). The foreach syntax will be used whenever possible in this book.
## return
Several keywords represent unconditional branching, which simply means that the branch happens without any test. These include return, break, continue, and a way to jump to a labeled statement which is similar to the goto in other languages. The return keyword has two purposes: It specifies what value a method will return (if it doesn’t have a void return value) and it causes the current method to exit, returning that value. The preceding test( ) method can be rewritten to take advantage of this:
```java
//: control/IfElse2.java
import static net.mindview.util.Print.*;
public class IfElse2 {
static int test(int testval, int target) {
if(testval > target)
return +1;
else if(testval < target)
return -1;
else
return 0; // Match
}
public static void main(String[] args) {
print(test(10, 5));
print(test(5, 10));
print(test(5, 5));
}
} /* Output:
-1
*///:~
```
There’s no need for else, because the method will not continue after executing a return. If you do not have a return statement in a method that returns void, there’s an implicit return at the end of that method, so it’s not always necessary to include a return statement. However, if your method states it will return anything other than void, you must ensure every code path will return a value. Exercise 6: (2) Modify the two test( ) methods in the previous two programs so that they take two extra arguments, begin and end, and so that testval is tested to see if it is within the range between (and including) begin and end.
## break and continue

<!--p122-->
You can also control the flow of the loop inside the body of any of the iteration statements by using break and continue. break quits the loop without executing the rest of the statements in the loop. continue stops the execution of the current iteration and goes back to the beginning of the loop to begin the next iteration. Controlling Execution This program shows examples of break and continue within for and while loops:
```java
//: control/BreakAndContinue.java
// Demonstrates break and continue keywords.
import static net.mindview.util.Range.*;
public class BreakAndContinue {
public static void main(String[] args) {
for(int i = 0; i < 100; i++) {
if(i == 74) break; // Out of for loop
if(i % 9 != 0) continue; // Next iteration
System.out.print(i + " ");
}
System.out.println();
// Using foreach:
for(int i : range(100)) {
if(i == 74) break; // Out of for loop
if(i % 9 != 0) continue; // Next iteration
System.out.print(i + " ");
}
System.out.println();
int i = 0;
// An "infinite loop":
while(true) {
i++;
int j = i * 27;
if(j == 1269) break; // Out of loop
if(i % 10 != 0) continue; // Top of loop
System.out.print(i + " ");
}
}
} /* Output:
0 9 18 27 36 45 54 63 72
0 9 18 27 36 45 54 63 72
10 20 30 40
*///:~
```

<!--p123-->
In the for loop, the value of i never gets to 100 because the break statement breaks out of the loop when i is 74. Normally, you’d use a break like this only if you didn’t know when the terminating condition was going to occur. The continue statement causes execution to go back to the top of the iteration loop (thus incrementing i) whenever i is not evenly divisible by 9. When it is, the value is printed. The second for loop shows the use of foreach, and that it produces the same results. Finally, you see an “infinite” while loop that would, in theory, continue forever. However, inside the loop there is a break statement that will break out of the loop. In addition, you’ll see that the continue statement moves control back to the top of the loop without completing anything after that continue statement. (Thus printing happens in the second loop only when the value of i is divisible by 10.) In the output, the value 0 is printed, because 0 % 9 produces 0. A second form of the infinite loop is for(;;). The compiler treats both while(true) and for(;;) in the same way, so whichever one you use is a matter of programming taste. Exercise 7: (1) Modify Exercise 1 so that the program exits by using the break keyword at value 99. Try using return instead. The infamous “goto” The goto keyword has been present in programming languages from the beginning. Indeed, goto was the genesis of program control in assembly language: “If condition A, then jump here; otherwise, jump there.” If you read the assembly code that is ultimately generated by virtually any compiler, you’ll see that program control contains many jumps (the Java compiler produces its own “assembly code,” but this code is run by the Java Virtual Machine rather than directly on a hardware CPU). A goto is a jump at the source-code level, and that’s what brought it into disrepute. If a program will always jump from one point to another, isn’t there some way to reorganize the code so the flow of control is not so jumpy? goto fell into true disfavor with the publication of the famous “Goto considered harmful” paper by Edsger Dijkstra, and since then goto- bashing has been a popular sport, with advocates of the cast-out keyword scurrying for cover. As is typical in situations like this, the middle ground is the most fruitful. The problem is not the use of goto, but the overuse of goto; in rare situations goto is actually the best way to structure control flow. Although goto is a reserved word in Java, it is not used in the language; Java has no goto. However, it does have something that looks a bit like a jump tied in with the break and continue keywords. It’s not a jump but rather a way to break out of an iteration statement. The reason it’s often thrown in with discussions of goto is because it uses the same mechanism: a label. A label is an identifier followed by a colon, like this:
```java
label1:
```
The only place a label is useful in Java is right before an iteration statement. And that means right before—it does no good to put any other statement between the label and the iteration. And the sole reason to put a label before an iteration is if you’re going to nest another iteration or a switch (which you’ll learn about shortly) inside it. That’s because the break and continue keywords will normally interrupt only the current loop, but when used with a label, they’ll interrupt the loops up to where the label exists:
```java
label1:
outer-iteration {
inner-iteration {
//...
break; // (1)
//...
continue; // (2)
//...
continue label1; // (3)
//...
break label1; // (4)
}
}
```

<!--p124-->
In (1), the break breaks out of the inner iteration and you end up in the outer iteration. In (2), the continue moves back to the beginning of the inner iteration. But in (3), the continue label1 breaks out of the inner iteration and the outer iteration, all the way back to label1. Then it does in fact continue the iteration, but starting at the outer iteration. In (4), the break label1 also breaks all the way out to label1, but it does not reenter the iteration. It actually does break out of both iterations. Controlling Execution Here is an example using for loops:

<!--p125-->
```java
//: control/LabeledFor.java
// For loops with "labeled break" and "labeled continue."
import static net.mindview.util.Print.*;
public class LabeledFor {
public static void main(String[] args) {
int i = 0;
outer: // Can’t have statements here
for(; true ;) { // infinite loop
inner: // Can’t have statements here
for(; i < 10; i++) {
print("i = " + i);
if(i == 2) {
print("continue");
continue;
}
if(i == 3) {
print("break");
i++; // Otherwise i never
// gets incremented.
break;
}
if(i == 7) {
print("continue outer");
i++; // Otherwise i never
// gets incremented.
continue outer;
}
if(i == 8) {
print("break outer");
break outer;
}
for(int k = 0; k < 5; k++) {
if(k == 3) {
print("continue inner");
continue inner;
}
}
}
}
// Can’t break or continue to labels here
}
} /* Output:
i = 0
continue inner
i = 1
continue inner
i = 2
continue
i = 3
break
i = 4
continue inner
i = 5
continue inner
i = 6
continue inner
i = 7
continue outer
i = 8
break outer
*///:~
```
Note that break breaks out of the for loop, and that the increment expression doesn’t occur until the end of the pass through the for loop. Since break skips the increment expression, the increment is performed directly in the case of i == 3. The continue outer statement in the case of i == 7 also goes to the top of the loop and also skips the increment, so it too is incremented directly. If not for the break outer statement, there would be no way to get out of the outer loop from within an inner loop, since break by itself can break out of only the innermost loop. (The same is true for continue.) Of course, in the cases where breaking out of a loop will also exit the method, you can simply use a return. Here is a demonstration of labeled break and continue statements with while loops:
```java
//: control/LabeledWhile.java
// While loops with "labeled break" and "labeled continue."
import static net.mindview.util.Print.*;
public class LabeledWhile {
public static void main(String[] args) {
int i = 0;
outer:
while(true) {
print("Outer while loop");
while(true) {
i++;
print("i = " + i);
if(i == 1) {
print("continue");
continue;
}
if(i == 3) {
print("continue outer");
continue outer;
}
if(i == 5) {
print("break");
break;
}
if(i == 7) {
print("break outer");
break outer;
}
}
}
}
} /* Output:
Outer while loop
i = 1
continue
i = 2
i = 3
continue outer
Outer while loop
i = 4
i = 5
break
Outer while loop
```

<!--p126-->
Controlling Execution
```java
i = 6
i = 7
break outer
*///:~
```
The same rules hold true for while: 1.A plain continue goes to the top of the innermost loop and continues. 2.A labeled continue goes to the label and reenters the loop right after that label. 3.A break “drops out of the bottom” of the loop. 4.A labeled break drops out of the bottom of the end of the loop denoted by the label. It’s important to remember that the only reason to use labels in Java is when you have nested loops and you want to break or continue through more than one nested level. In Dijkstra’s “Goto considered harmful” paper, what he specifically objected to was the labels, not the goto. He observed that the number of bugs seems to increase with the number of labels in a program, and that labels and gotos make programs difficult to analyze. Note that Java labels don’t suffer from this problem, since they are constrained in their placement and can’t be used to transfer control in an ad hoc manner. It’s also interesting to note that this is a case where a language feature is made more useful by restricting the power of the statement.
## switch
The switch is sometimes called a selection statement. The switch statement selects from among pieces of code based on the value of an integral expression. Its general form is:
```java
switch(integral-selector) {
case integral-value1 : statement; break;
case integral-value2 : statement; break;
case integral-value3 : statement; break;
case integral-value4 : statement; break;
case integral-value5 : statement; break;
// ...
default: statement;
}
```

<!--p127-->
Integral-selector is an expression that produces an integral value. The switch compares the result of integral-selector to each integral-value. If it finds a match, the corresponding statement (a single statement or multiple statements; braces are not required) executes. If no match occurs, the default statement executes. You will notice in the preceding definition that each case ends with a break, which causes execution to jump to the end of the switch body. This is the conventional way to build a switch statement, but the break is optional. If it is missing, the code for the following case statements executes until a break is encountered. Although you don’t usually want this kind of behavior, it can be useful to an experienced programmer. Note that the last statement, following the default, doesn’t have a break because the execution just falls through to where the break would have taken it anyway. You could put a break at the end of the default statement with no harm if you considered it important for style’s sake. The switch statement is a clean way to implement multiway selection (i.e., selecting from among a number of different execution paths), but it requires a selector that evaluates to an integral value, such as int or char. If you want to use, for example, a string or a floating point number as a selector, it won’t work in a switch statement. For non-integral types, you must use a series of if statements. At the end of the next chapter, you’ll see that Java SE5’s new enum feature helps ease this restriction, as enums are designed to work nicely with switch. Here’s an example that creates letters randomly and determines whether they’re vowels or consonants:
```java
//: control/VowelsAndConsonants.java
// Demonstrates the switch statement.
import java.util.*;
import static net.mindview.util.Print.*;
public class VowelsAndConsonants {
public static void main(String[] args) {
Random rand = new Random(47);
for(int i = 0; i < 100; i++) {
int c = rand.nextInt(26) + ‘a’;
printnb((char)c + ", " + c + ": ");
switch(c) {
case ‘a’:
case ‘e’:
case ‘i’:
case ‘o’:
case ‘u’: print("vowel");
break;
case ‘y’:
case ‘w’: print("Sometimes a vowel");
break;
default: print("consonant");
}
}
}
} /* Output:
y, 121: Sometimes a vowel
n, 110: consonant
z, 122: consonant
b, 98: consonant
r, 114: consonant
n, 110: consonant
y, 121: Sometimes a vowel
g, 103: consonant
c, 99: consonant
f, 102: consonant
o, 111: vowel
w, 119: Sometimes a vowel
z, 122: consonant
...
*///:~
```

<!--p128-->
Since Random.nextInt(26) generates a value between 0 and 26, you need only add an offset of ‘a’ to produce the lowercase letters. The single-quoted characters in the case statements also produce integral values that are used for comparison. Notice how the cases can be “stacked” on top of each other to provide multiple matches for a particular piece of code. You should also be aware that it’s essential to put the break statement at the end of a particular case; otherwise, control will simply drop through and continue processing on the next case. Controlling Execution In the statement:
```java
int c = rand.nextInt(26) + ‘a’;
```
Random.nextInt( ) produces a random int value from 0 to 25, which is added to the value of ‘a’. This means that ‘a’ is automatically converted to an int to perform the addition. In order to print c as a character, it must be cast to char; otherwise, you’ll produce integral output. Exercise 8:(2) Create a switch statement that prints a message for each case, and put the switch inside a for loop that tries each case. Put a break after each case and test it, then remove the breaks and see what happens. Exercise 9:(4) A Fibonacci sequence is the sequence of numbers 1, 1, 2, 3, 5, 8, 13, 21, 34, and so on, where each number (from the third on) is the sum of the previous two. Create a method that takes an integer as an argument and displays that many Fibonacci numbers starting from the beginning, e.g., If you run java Fibonacci 5 (where Fibonacci is the name of the class) the output will be: 1, 1, 2, 3, 5. Exercise 10: (5) A vampire number has an even number of digits and is formed by multiplying a pair of numbers containing half the number of digits of the result. The digits are taken from the original number in any order. Pairs of trailing zeroes are not allowed. Examples include: 1260 = 21 * 60 1827 = 21 * 87 2187 = 27 * 81 Write a program that finds all the 4-digit vampire numbers. (Suggested by Dan Forhan.) Summary This chapter concludes the study of fundamental features that appear in most programming languages: calculation, operator precedence, type casting, and selection and iteration. Now you’re ready to begin taking steps that move you closer to the world of object-oriented programming. The next chapter will cover the important issues of initialization and cleanup of objects, followed in the subsequent chapter by the essential concept of implementation hiding. Solutions to selected exercises can be found in the electronic document The Thinking in Java Annotated Solution Guide, available for sale from www.MindView.net.