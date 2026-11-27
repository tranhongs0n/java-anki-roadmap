# 20. Annotations (printed p761-796)


<!--p783-->

<!--p784-->
Annotations Annotations (also known as metadata) provide a formalized way to add information to your code so that you can easily use that data at some later point.1 Annotations are partly motivated by a general trend toward combining metadata with source-code files, instead of keeping it in external documents. They are also a response to feature pressure from other languages like C#. Annotations are one of the fundamental language changes introduced in Java SE5. They provide information that you need to fully describe your program, but that cannot be expressed in Java. Thus, annotations allow you to store extra information about your program in a format that is tested and verified by the compiler. Annotations can be used to generate descriptor files or even new class definitions and help ease the burden of writing "boilerplate" code. Using annotations, you can keep this metadata in the Java source code, and have the advantage of cleaner looking code, compile-time type checking and the annotation API to help build processing tools for your annotations. Although a few types of metadata come predefined in Java SE5, in general the kind of annotations you add and what you do with them are entirely up to you. The syntax of annotations is reasonably simple and consists mainly of the addition of the @ symbol to the language. Java SE5 contains three generalpurpose built-in annotations, defined in java.lang: • @Override, to indicate that a method definition is intended to override a method in the base class. This generates a compiler error if you accidentally misspell the method name or give an improper signature.2 • @Deprecated, to produce a compiler warning if this element is used. • @SuppressWarnings, to turn off inappropriate compiler warnings. This annotation is allowed but not supported in earlier releases of Java SE5 (it was ignored). Four additional annotation types support the creation of new annotations; you will learn about these in this chapter. Anytime you create descriptor classes or interfaces that involve repetitive work, you can usually use annotations to automate and simplify the process. Much of the extra work in Enterprise JavaBeans (EJBs), for example, is eliminated through the use of annotations in EJB3.0. Annotations can replace existing systems like XDoclet, which is an independent doclet tool (see the supplement at http://MindView.net/Books/BetterJava) that is specifically designed for creating annotation-style doclets. In contrast, annotations are true language constructs and hence are structured, and are type-checked at compile time. Keeping all the information in the actual source code and not in comments makes the code neater and easier to maintain. By using and extending the annotation API and tools, or with external bytecode manipulation 1 Jeremy Meyer came to Crested Butte and spent two weeks with me working on this chapter. His help was invaluable. 2 This was no doubt inspired by a similar feature in C#. The C# feature is a keyword and not an annotation, and is enforced by the compiler. That is, when you override a method in C#, you must use the override keyword, whereas in Java the (©Override annotation is optional. libraries as you will see in this chapter, you can perform powerful inspection and manipulation of your source code as well as the bytecode. Basic syntax In the example below, the method testExecute( ) is annotated with @Test. This doesn’t do anything by itself, but the compiler will ensure that you have a definition for the @Test annotation in your build path. As you will see later in the chapter, you can create a tool which runs this method for you via reflection.
```java
//: annotations/Testable.java
package annotations;
import net.mindview.atunit.*;
public class Testable {
public void execute() {
System.out.println("Executing..");
}
@Test void testExecute() { execute(); }
} ///:~
```
Annotated methods are no different from other methods. The @Test annotation in this example can be used in combination with any of the modifiers like public or static or void. Syntactically, annotations are used in much the same way as modifiers. Defining annotations Here is the definition of the annotation above. You can see that annotation definitions look a lot like interface definitions. In fact, they compile to class files like any other Java interface:
```java
//: net/mindview/atunit/Test.java
// The @Test tag.
package net.mindview.atunit;
import java.lang.annotation.*;
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Test {} ///:~
```

<!--p785-->
Apart from the @ symbol, the definition of @Test is much like that of an empty interface. An annotation definition also requires the meta-annotations @Target and (@Retention. @Target defines where you can apply this annotation (a method or a field, for example). @Retention defines whether the annotations are available in the source code (SOURCE), in the class files (CLASS), or at run time (RUNTIME). Annotations will usually contain elements to specify values in your annotations. A program or tool can use these parameters when processing your annotations. Elements look like interface methods, except that you can declare default values. An annotation without any elements, such as @Test above, is called a marker annotation. Here is a simple annotation that tracks use cases in a project. Programmers annotate each method or set of methods which fulfill the requirements of a particular use case. A project manager can get an idea of project progress by counting the implemented use cases, and developers maintaining the project can easily find use cases if they need to update or debug business rules within the system.
```java
//: annotations/UseCase.java
import java.lang.annotation.*;
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface UseCase {
public int id();
public String description() default "no description";
} ///:~
```
Notice that id and description resemble method declarations. Because id is type-checked by the compiler, it is a reliable way of linking a tracking database to the use case document and the source code. The element description has a default value which is picked up by the annotation processor if no value is specified when a method is annotated. Here is a class with three methods annotated as use cases:
```java
//: annotations/PasswordUtils.java
import java.util.*;
public class PasswordUtils {
@UseCase(id = 47, description =
"Passwords must contain at least one numeric")
public boolean validatePassword(String password) {
return (password.matches("\\w*\\d\\w*"));
}
@UseCase(id = 48)
public String encryptPassword(String password) {
return new StringBuilder(password).reverse().toString();
}
@UseCase(id = 49, description =
"New passwords can’t equal previously used ones")
public boolean checkForNewPassword(
List<String> prevPasswords, String password) {
return !prevPasswords.contains(password);
}
} ///:~
```

<!--p786-->

<!--p787-->
The values of the annotation elements are expressed as name-value pairs in parentheses after the @UseCase declaration. The annotation for encryptPassword( ) is not passed a value for the description element here, so the default value defined in the ©interface UseCase will appear when the class is run through an annotation processor. You could imagine using a system like this in order to "sketch" out your system, and then filling in the functionality as you build it. Meta-annotations There are currently only three standard annotations (described earlier) and four meta- annotations defined in the Java language. The meta-annotations are for annotating annotations: @Target Where this annotation can be applied. The possible ElementType arguments are: CONSTRUCTOR:Constructor declaration FIELD:Field declaration (includes enum constants) LOCAL_VARIABLE:Local variable declaration METHOD:Method declaration Annotations PACKAGE: Package declaration PARAMETER:Parameter declaration TYPE:Class, interface (including annotation type), or enum declaration @Retention How long the annotation information is kept. The possible RetentionPolicy arguments are: SOURCE: Annotations are discarded by the compiler. CLASS: Annotations are available in the class file by the compiler but can be discarded by the VM. RUNTIME:Annotations are retained by the VM at run time, so they may be read reflectively. @Documented Include this annotation in the Javadocs. @Inherited Allow subclasses to inherit parent annotations. Most of the time, you will be defining your own annotations and writing your own processors to deal with them. Writing annotation processors Without tools to read them, annotations are hardly more useful than comments. An important part of the process of using annotations is to create and use annotation processors. Java SE5 provides extensions to the reflection API to help you create these tools. It also provides an external tool called apt to help you parse Java source code with annotations. Here is a very simple annotation processor that reads the annotated PasswordUtils class and uses reflection to look for @UseCase tags. Given a list of id values, it lists the use cases it finds and reports any that are missing:
```java
//: annotations/UseCaseTracker.java
import java.lang.reflect.*;
import java.util.*;
public class UseCaseTracker {
public static void
trackUseCases(List<Integer> useCases, Class<?> cl) {
for(Method m : cl.getDeclaredMethods()) {
UseCase uc = m.getAnnotation(UseCase.class);
if(uc != null) {
System.out.println("Found Use Case:" + uc.id() +
" " + uc.description());
useCases.remove(new Integer(uc.id()));
}
}
for(int i : useCases) {
System.out.println("Warning: Missing use case-" + i);
}
}
public static void main(String[] args) {
List<Integer> useCases = new ArrayList<Integer>();
Collections.addAll(useCases, 47, 48, 49, 50);
trackUseCases(useCases, PasswordUtils.class);
}
} /* Output:
Found Use Case:47 Passwords must contain at least one numeric
Found Use Case:48 no description
Found Use Case:49 New passwords can’t equal previously used ones
Warning: Missing use case-50
*///:~
```

<!--p788-->
This uses both the reflection method getDeclaredMethods( ) and the method getAnnotation( ), which comes from the AnnotatedElement interface (classes like Class, Method and Field all implement this interface). This method returns the annotation object of the specified type, in this case "UseCase." If there are no annotations of that particular type on the annotated method, a null value is returned. The element values are extracted by calling id( ) and description( ). Remember that no description was specified in the annotation for the encryptPassword( ) method, so the processor above finds the default value "no description"when it calls the description( ) method on that particular annotation. Annotation elements The @UseCase tag defined in UseCase.java contains the int element id and String element description. Here is a list of the allowed types for annotation elements: Annotations • All primitives (int, float, boolean etc.) • String • Class • Enums • Annotations • Arrays of any of the above The compiler will report an error if you try to use any other types. Note that you are not allowed to use any of the wrapper classes, but because of autoboxing this isn’t really a limitation. You can also have elements that are themselves annotations. As you will see a bit later, nested annotations can be very helpful. Default value constraints The compiler is quite picky about default element values. No element can have an unspecified value. This means that elements must either have default values or values provided by the class that uses the annotation. There is another restriction, which is that none of the non-primitive type elements are allowed to take null as a value, either when declared in the source code or when defined as a default value in the annotation interface. This makes it hard to write a processor that acts on the presence or absence of an element, because every element is effectively present in every annotation declaration. You can get around this by checking for specific values, like empty strings or negative values:
```java
//: annotations/SimulatingNull.java
import java.lang.annotation.*;
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface SimulatingNull {
public int id() default -1;
public String description() default "";
} ///:~
```

<!--p789-->
This is a typical idiom in annotation definitions. Generating external files Annotations are especially useful when working with frameworks that require some sort of additional information to accompany your source code. Technologies like Enterprise JavaBeans (prior to EJB3) require numerous interfaces and deployment descriptors which are "boilerplate" code, defined in the same way for every bean. Web services, custom tag libraries and object/relational mapping tools like Toplink and Hibernate often require XML descriptors that are external to the code. After defining a Java class, the programmer must undergo the tedium of respecifying information like the name, package and so on— information that already exists in the original class. Whenever you use an external descriptor file, you end up with two separate sources of information about a class, which usually leads to code synchronization problems. This also requires that programmers working on the project must know about editing the descriptor as well as how to write Java programs. Suppose you want to provide basic object/relational mapping functionality to automate the creation of a database table in order to store a JavaBean. You could use an XML descriptor file to specify the name of the class, each member, and information about its database mapping. Using annotations, however, you can keep all of the information in the JavaBean source file. To do this, you need annotations to define the name of the database table associated with the bean, the columns, and the SQL types to map to the bean’s properties. Here is an annotation for a bean that tells the annotation processor that it should create a database table:
```java
//: annotations/database/DBTable.java
package annotations.database;
import java.lang.annotation.*;
@Target(ElementType.TYPE) // Applies to classes only
@Retention(RetentionPolicy.RUNTIME)
public @interface DBTable {
public String name() default "";
} ///:~
```
Each ElementType that you specify in the @Target annotation is a restriction that tells the compiler that your annotation can only be applied to that particular type. You can specify a single value of the enum ElementType, or you can specify a comma-separated list of any combination of values. If you want to apply the annotation to any ElementType, you can leave out the @Target annotation altogether, although this is uncommon. Note that @DBTable has a name( ) element so that the annotation can supply a name for the database table that the processor will create. Here are the annotations for the JavaBean fields:
```java
//: annotations/database/Constraints.java
package annotations.database;
import java.lang.annotation.*;
@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Constraints {
boolean primaryKey() default false;
boolean allowNull() default true;
boolean unique() default false;
} ///:~
//: annotations/database/SQLString.java
package annotations.database;
import java.lang.annotation.*;
@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
public @interface SQLString {
int value() default 0;
String name() default "";
Constraints constraints() default @Constraints;
} ///:~
//: annotations/database/SQLInteger.java
package annotations.database;
import java.lang.annotation.*;
@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
```

<!--p790-->
Annotations
```java
public @interface SQLInteger {
String name() default "";
Constraints constraints() default @Constraints;
} ///:~
```
The @Constraints annotation allows the processor to extract the metadata about the database table. This represents a small subset of the constraints generally offered by databases, but it gives you the general idea. The elements primaryKey( ), allowNull( ) and unique( ) are given sensible default values so that in most cases a user of the annotation won’t have to type too much. The other two (@interfaces define SQL types. Again, for this framework to be more useful, you need to define an annotation for each additional SQL type. Here, two types will be enough. These types each have a name( ) element and a constraints( ) element. The latter makes use of the nested annotation feature to embed the information about the column type’s database constraints. Note that the default value for the contraints( ) element is @Constraints. Since there are no element values specified in parentheses after this annotation type, the default value of constraints( ) is actually an @Constraints annotation with its own default values set. To make a nested @Constraints annotation with uniqueness set to true by default, you can define its element like this:
```java
//: annotations/database/Uniqueness.java
// Sample of nested annotations
package annotations.database;
public @interface Uniqueness {
Constraints constraints()
default @Constraints(unique=true);
} ///:~
```
Here is a simple bean that uses these annotations:
```java
//: annotations/database/Member.java
package annotations.database;
@DBTable(name = "MEMBER")
public class Member {
@SQLString(30) String firstName;
@SQLString(50) String lastName;
@SQLInteger Integer age;
@SQLString(value = 30,
constraints = @Constraints(primaryKey = true))
String handle;
static int memberCount;
public String getHandle() { return handle; }
public String getFirstName() { return firstName; }
public String getLastName() { return lastName; }
public String toString() { return handle; }
public Integer getAge() { return age; }
} ///:~
```

<!--p791-->
The @DBTable class annotation is given the value "MEMBER", which will be used as the table name. The bean properties, firstName and lastName, are both annotated with @SQLStrings and have element values of 30 and 50, respectively. These annotations are interesting for two reasons: First, they use the default value on the nested (@Constraints annotation, and second, they use a shortcut feature. If you define an element on an annotation with the name value, then as long as it is the only element type specified you don’t need to use the name-value pair syntax; you can just specify the value in parentheses. This can be applied to any of the legal element types. Of course this limits you to naming your element "value" but in the case above, it does allow for the semantically meaningful and easy- to-read annotation specification:
```java
@SQLString(30)
```
The processor will use this value to set the size of the SQL column that it will create. As neat as the default-value syntax is, it quickly becomes complex. Look at the annotation on the field handle. This has an @SQLString annotation, but it also needs to be a primary key on the database, so the element type primaryKey must be set on the nested @Constraint annotation. This is where it gets messy. You are now forced to use the rather long-winded namevalue pair form for this nested annotation, respecifying the element name and the @interface name. But because the specially named element value is no longer the only element value being specified, you can’t use the shortcut form. As you can see, the result is not pretty. Alternative solutions There are other ways of creating annotations for this task. You could, for example, have a single annotation class called @TableColumn with an enum element which defines values like STRING, INTEGER, FLOAT, etc. This eliminates the need for an @interface for each SQL type, but makes it impossible to qualify your types with additional elements like size, or precision, which is probably more useful. You could also use a String element to describe the actual SQL type, e.g., "VARCHAR(30)" or "INTEGER". This does allow you to qualify the types, but it ties up the mapping from Java type to SQL type in your code, which is not good design. You don’t want to have to recompile classes if you change databases; it would be more elegant just to tell your annotation processor that you are using a different "flavor" of SQL, and it let it take that into account when processing the annotations. A third workable solution is to use two annotation types together, @Constraints and the relevant SQL type (for example, @SQLInteger), to annotate the desired field. This is slightly messy but the compiler allows as many different annotations as you like on an annotation target. Note that when using multiple annotations, you cannot use the same annotation twice. Annotations don’t support inheritance You cannot use the extends keyword with @interfaces. This is a pity, because an elegant solution would have been to define an annotation @TableColumn, as suggested above, with a nested annotation of type @SQLType. That way, you could inherit all your SQL types, like @SQLInteger and @SQLString, from @SQLType. This would reduce typing and neaten the syntax. There doesn’t seem to be any suggestion of annotations supporting inheritance in future releases, so the examples above seem to be the best you can do under the circumstances. Implementing the processor Here is an example of an annotation processor which reads in a class file, checks for its database annotations and generates the SQL command for making the database:
```java
//: annotations/database/TableCreator.java
// Reflection-based annotation processor.
// {Args: annotations.database.Member}
```

<!--p792-->
Annotations

<!--p793-->
```java
package annotations.database;
import java.lang.annotation.*;
import java.lang.reflect.*;
import java.util.*;
public class TableCreator {
public static void main(String[] args) throws Exception {
if(args.length < 1) {
System.out.println("arguments: annotated classes");
System.exit(0);
}
for(String className : args) {
Class<?> cl = Class.forName(className);
DBTable dbTable = cl.getAnnotation(DBTable.class);
if(dbTable == null) {
System.out.println(
"No DBTable annotations in class " + className);
continue;
}
String tableName = dbTable.name();
// If the name is empty, use the Class name:
if(tableName.length() < 1)
tableName = cl.getName().toUpperCase();
List<String> columnDefs = new ArrayList<String>();
for(Field field : cl.getDeclaredFields()) {
String columnName = null;
Annotation[] anns = field.getDeclaredAnnotations();
if(anns.length < 1)
continue; // Not a db table column
if(anns[0] instanceof SQLInteger) {
SQLInteger sInt = (SQLInteger) anns[0];
// Use field name if name not specified
if(sInt.name().length() < 1)
columnName = field.getName().toUpperCase();
else
columnName = sInt.name();
columnDefs.add(columnName + " INT" +
getConstraints(sInt.constraints()));
}
if(anns[0] instanceof SQLString) {
SQLString sString = (SQLString) anns[0];
// Use field name if name not specified.
if(sString.name().length() < 1)
columnName = field.getName().toUpperCase();
else
columnName = sString.name();
columnDefs.add(columnName + " VARCHAR(" +
sString.value() + ")" +
getConstraints(sString.constraints()));
}
StringBuilder createCommand = new StringBuilder(
"CREATE TABLE " + tableName + "(");
for(String columnDef : columnDefs)
createCommand.append("\n " + columnDef + ",");
// Remove trailing comma
String tableCreate = createCommand.substring(
0, createCommand.length() - 1) + ");";
System.out.println("Table Creation SQL for " +
className + " is :\n" + tableCreate);
}
}
}
private static String getConstraints(Constraints con) {
```
Annotations
```java
String constraints = "";
if(!con.allowNull())
constraints += " NOT NULL";
if(con.primaryKey())
constraints += " PRIMARY KEY";
if(con.unique())
constraints += " UNIQUE";
return constraints;
}
} /* Output:
Table Creation SQL for annotations.database.Member is :
CREATE TABLE MEMBER(
FIRSTNAME VARCHAR(30));
Table Creation SQL for annotations.database.Member is :
CREATE TABLE MEMBER(
FIRSTNAME VARCHAR(30),
LASTNAME VARCHAR(50));
Table Creation SQL for annotations.database.Member is :
CREATE TABLE MEMBER(
FIRSTNAME VARCHAR(30),
LASTNAME VARCHAR(50),
AGE INT);
Table Creation SQL for annotations.database.Member is :
CREATE TABLE MEMBER(
FIRSTNAME VARCHAR(30),
LASTNAME VARCHAR(50),
AGE INT,
HANDLE VARCHAR(30) PRIMARY KEY);
*///:~
```

<!--p794-->
The main( ) method cycles through each of the class names on the command line. Each class is loaded using forName( ) and checked to see if it has the @DBTable annotation on it with getAnnotation(DBTable.class). If it does, then the table name is found and stored. All of the fields in the class are then loaded and checked using getDeclaredAnnotations( ). This method returns an array of all of the defined annotations for a particular method. The instanceof operator is used to determine if these annotations are of type @SQLInteger and @SQLString, and in each case the relevant String fragment is then created with the name of the table column. Note that because there is no inheritance of annotation interfaces, using getDeclaredAnnotations( ) is the only way you can approximate polymorphic behavior. The nested @Constraint annotation is passed to the getConstraints( ) which builds up a String containing the SQL constraints. It is worth mentioning that the technique shown above is a somewhat naive way of defining an object/relational mapping. Having an annotation of type @DBTable which takes the table name as a parameter forces you to recompile your Java code if you want to change the table name. This might not be desirable. There are many available frameworks for mapping objects to relational databases, and more and more of them are making use of annotations. Exercise 1:(2) Implement more SQL types in the database example. Project3Modify the database example so that it connects and interacts with a real database using JDBC. Project: Modify the database example so that it creates conformant XML files rather than writing SQL code. 3 Projects are suggestions to be used (for example) as term projects. Solutions to projects are not included in the solution guide.
## Using apt to process annotations
The annotation processing tool apt is Sun’s first version of a tool that aids the processing of annotations. Because it is an early incarnation, the tool is still a little primitive, but it has features which can make your life easier. Like javac, apt is designed to be run on Java source files rather than compiled classes. By default, apt compiles the source files when it has finished processing them. This is useful if you are automatically creating new source files as part of your build process. In fact, apt checks newly created source files for annotations and compiles them all in the same pass. When your annotation processor creates a new source file, that file is itself checked for annotations in a new round (as it is referred to in the documentation) of processing. The tool will continue round after round of processing until no more source files are being created. It then compiles all of the source files. Each annotation you write will need its own processor, but the apt tool can easily group several annotation processors together. It allows you to specify multiple classes to be processed, which is a lot easier than having to iterate through File classes yourself. You can also add listeners to receive notification of when an annotation processing round is complete. At the time of this writing, apt is not available as an Ant task (see the supplement at http://MindView.net/Books/BetterJava), but it can obviously be run as an external task from Ant in the meantime. In order to compile the annotation processors in this section you must have tools.jar in your classpath; this library also contains the the com.sun.mirror.* interfaces. apt works by using an AnnotationProcessorFactory to create the right kind of annotation processor for each annotation it finds. When you run apt, you specify either a factory class or a classpath where it can find the factories it needs. If you don’t do this, apt will embark on an arcane discovery process, the details of which can be found in the Developing an Annotation Processor section of Sun’s documentation. When you create an annotation processor for use with apt, you can’t use the reflection features in Java because you are working with source code, not compiled classes.4The mirror API5 solves this problem by allowing you to view methods, fields and types in uncompiled source code. Here is an annotation that can be used to extract the public methods from a class and turn them into an interface:
```java
//: annotations/ExtractInterface.java
// APT-based annotation processing.
package annotations;
import java.lang.annotation.*;
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.SOURCE)
public @interface ExtractInterface {
public String value();
} ///:~
```

<!--p795-->
4 However, using the non-standard -XclassesAsDecls option, you may work with annotations that are in compiled classes. 5 The Java designers coyly suggest that a mirror is where you find a reflection. The RetentionPolicy is SOURCE because there is no point in keeping this annotation in the class file after we have extracted the interface from the class. The following class provides a public method which can become part of a useful interface:
```java
//: annotations/Multiplier.java
// APT-based annotation processing.
package annotations;
@ExtractInterface("IMultiplier")
public class Multiplier {
public int multiply(int x, int y) {
int total = 0;
for(int i = 0; i < x; i++)
total = add(total, y);
return total;
}
private int add(int x, int y) { return x + y; }
public static void main(String[] args) {
Multiplier m = new Multiplier();
System.out.println("11*16 = " + m.multiply(11, 16));
}
} /* Output:
11*16 = 176
*///:~
```
The Multiplier class (which only works with positive integers) has a multiply( ) method which calls the private add( ) method numerous times to perform multiplication. The add( ) method is not public, so is not part of the interface. The annotation is given the value of IMultiplier, which is the name of the interface to create. Now you need a processor to do the extraction:
```java
//: annotations/InterfaceExtractorProcessor.java
// APT-based annotation processing.
// {Exec: apt -factory
// annotations.InterfaceExtractorProcessorFactory
// Multiplier.java -s ../annotations}
package annotations;
import com.sun.mirror.apt.*;
import com.sun.mirror.declaration.*;
import java.io.*;
import java.util.*;
public class InterfaceExtractorProcessor
implements AnnotationProcessor {
private final AnnotationProcessorEnvironment env;
private ArrayList<MethodDeclaration> interfaceMethods =
new ArrayList<MethodDeclaration>();
public InterfaceExtractorProcessor(
AnnotationProcessorEnvironment env) { this.env = env; }
public void process() {
for(TypeDeclaration typeDecl :
env.getSpecifiedTypeDeclarations()) {
ExtractInterface annot =
typeDecl.getAnnotation(ExtractInterface.class);
if(annot == null)
break;
for(MethodDeclaration m : typeDecl.getMethods())
if(m.getModifiers().contains(Modifier.PUBLIC) &&
!(m.getModifiers().contains(Modifier.STATIC)))
interfaceMethods.add(m);
if(interfaceMethods.size() > 0) {
```

<!--p796-->
Annotations
```java
try {
PrintWriter writer =
env.getFiler().createSourceFile(annot.value());
writer.println("package " +
typeDecl.getPackage().getQualifiedName() +";");
writer.println("public interface " +
annot.value() + " {");
for(MethodDeclaration m : interfaceMethods) {
writer.print(" public ");
writer.print(m.getReturnType() + " ");
writer.print(m.getSimpleName() + " (");
int i = 0;
for(ParameterDeclaration parm :
m.getParameters()) {
writer.print(parm.getType() + " " +
parm.getSimpleName());
if(++i < m.getParameters().size())
writer.print(", ");
}
writer.println(");");
}
writer.println("}");
writer.close();
} catch(IOException ioe) {
throw new RuntimeException(ioe);
}
}
}
}
} ///:~
```
The process( ) method is where all the work is done. The MethodDeclaration class and its getModifiers( ) method are used to identify the public methods (but ignore the static ones) of the class being processed. If any are found, they are stored in an ArrayList and used to create the methods of a new interface definition in a .java file. Notice that an AnnotationProcessorEnvironment object is passed into the constructor. You can query this object for all of the types (class definitions) that the apt tool is processing, and you can use it to get a Messager object and a Filer object. The Messager enables you to report messages to the user, e.g., any errors that might have occurred with the processing and where they are in the source code. The Filer is a kind of PrintWriter through which you will create new files. The main reason that you use a Filer object, rather than a plain PrintWriter, is that it allows apt to keep track of any new files that you create, so it can check them for annotations and compile them if it needs to. You will also see that the method createSourceFile( ) opens an ordinary output stream with the correct name for your Java class or interface. There isn’t any support for creating Java language constructs, so you have to generate the Java source code using the somewhat primitive print( ) and println( ) methods. This means making sure that your brackets match up and that your code is syntactically correct. process( ) is called by the apt tool, which needs a factory to provide the right processor:

<!--p797-->
```java
//: annotations/InterfaceExtractorProcessorFactory.java
// APT-based annotation processing.
package annotations;
import com.sun.mirror.apt.*;
import com.sun.mirror.declaration.*;
import java.util.*;
public class InterfaceExtractorProcessorFactory
implements AnnotationProcessorFactory {
public AnnotationProcessor getProcessorFor(
Set<AnnotationTypeDeclaration> atds,
AnnotationProcessorEnvironment env) {
return new InterfaceExtractorProcessor(env);
}
public Collection<String> supportedAnnotationTypes() {
return
Collections.singleton("annotations.ExtractInterface");
}
public Collection<String> supportedOptions() {
return Collections.emptySet();
}
} ///:~
```
There are only three methods on the AnnotationProcessorFactory interface. As you can see, the one which provides the processor is getProcessorFor( ), which takes a Set of type declarations (the Java classes that the apt tool is being run against), and the AnnotationProcessorEnvironment object, which you have already seen being passed through to the processor. The other two methods, supportedAnnotationTypes( ) and supportedOptions( ), are there so you can check that you have processors for all of the annotations found by apt and that you support all options specified at the command prompt. The getProcessorFor( ) method is particularly important because if you don’t return the full class name of your annotation type in the String collection, apt will warn you that there is no relevant processor and exit without doing anything. The processor and factory are in the package annotations, so for the directory structure above, the command line is embedded in the ‘Exec’comment tag at the beginning of InterfaceExtractorProcessor.java. This tells apt to use the factory class defined above and process the file Multiplier.java. The -s option specifies that any new files must be created in the directory annotations. The generated IMultiplier.java file, as you might guess by looking at the println( ) statements in the processor above, looks like this:
```java
package annotations;
public interface IMultiplier {
public int multiply (int x, int y);
}
```
This file will also be compiled by apt, so you will see the file IMultiplier.class in the same directory. Exercise 2:(3) Add support for division to the interface extractor.
## Using the Visitor pattern with apt

<!--p798-->
Processing annotations can become complex. The example above is a relatively simple annotation processor and only interprets one annotation, but still requires a fair amount of complexity to make it work. To prevent the complexity from scaling up badly when you have more annotations and more processors, the mirror API provides classes to support the Visitor design pattern. Visitor is one of the classic design patterns from the book Design Patterns by Gamma et al., and you can also find a more a detailed explanation in Thinking in Patterns. A Visitor traverses a data structure or collection of objects, performing an operation on each one. The data structure need not be ordered, and the operation that you perform on each object will be specific to its type. This decouples the operations from the objects themselves, meaning that you can add new operations without adding methods to the class definitions. Annotations This makes it useful for processing annotations, because a Java class can be thought of as a collection of objects such as TypeDeclarations, FieldDeclarations, MethodDeclarations, and so on. When you use the apt tool with the Visitor pattern, you provide a Visitor class which has a method for handling each type of declaration that you visit. Thus you can implement appropriate behavior for annotations on methods, classes, fields and so on. Here is the SQL table generator again, this time using a factory and a processor that makes use of the Visitor pattern:

<!--p799-->
```java
//: annotations/database/TableCreationProcessorFactory.java
// The database example using Visitor.
// {Exec: apt -factory
// annotations.database.TableCreationProcessorFactory
// database/Member.java -s database}
package annotations.database;
import com.sun.mirror.apt.*;
import com.sun.mirror.declaration.*;
import com.sun.mirror.util.*;
import java.util.*;
import static com.sun.mirror.util.DeclarationVisitors.*;
public class TableCreationProcessorFactory
implements AnnotationProcessorFactory {
public AnnotationProcessor getProcessorFor(
Set<AnnotationTypeDeclaration> atds,
AnnotationProcessorEnvironment env) {
return new TableCreationProcessor(env);
}
public Collection<String> supportedAnnotationTypes() {
return Arrays.asList(
"annotations.database.DBTable",
"annotations.database.Constraints",
"annotations.database.SQLString",
"annotations.database.SQLInteger");
}
public Collection<String> supportedOptions() {
return Collections.emptySet();
}
private static class TableCreationProcessor
implements AnnotationProcessor {
private final AnnotationProcessorEnvironment env;
private String sql = "";
public TableCreationProcessor(
AnnotationProcessorEnvironment env) {
this.env = env;
}
public void process() {
for(TypeDeclaration typeDecl :
env.getSpecifiedTypeDeclarations()) {
typeDecl.accept(getDeclarationScanner(
new TableCreationVisitor(), NO_OP));
sql = sql.substring(0, sql.length() - 1) + ");";
System.out.println("creation SQL is :\n" + sql);
sql = "";
}
}
private class TableCreationVisitor
extends SimpleDeclarationVisitor {
public void visitClassDeclaration(
ClassDeclaration d) {
DBTable dbTable = d.getAnnotation(DBTable.class);
if(dbTable != null) {
sql += "CREATE TABLE ";
sql += (dbTable.name().length() < 1)
? d.getSimpleName().toUpperCase()
: dbTable.name();
sql += " (";
}
}
public void visitFieldDeclaration(
FieldDeclaration d) {
String columnName = "";
if(d.getAnnotation(SQLInteger.class) != null) {
SQLInteger sInt = d.getAnnotation(
SQLInteger.class);
// Use field name if name not specified
if(sInt.name().length() < 1)
columnName = d.getSimpleName().toUpperCase();
else
columnName = sInt.name();
sql += "\n " + columnName + " INT" +
getConstraints(sInt.constraints()) + ",";
}
if(d.getAnnotation(SQLString.class) != null) {
SQLString sString = d.getAnnotation(
SQLString.class);
// Use field name if name not specified.
if(sString.name().length() < 1)
columnName = d.getSimpleName().toUpperCase();
else
columnName = sString.name();
sql += "\n " + columnName + " VARCHAR(" +
sString.value() + ")" +
getConstraints(sString.constraints()) + ",";
}
}
private String getConstraints(Constraints con) {
String constraints = "";
if(!con.allowNull())
constraints += " NOT NULL";
if(con.primaryKey())
constraints += " PRIMARY KEY";
if(con.unique())
constraints += " UNIQUE";
return constraints;
}
}
}
} ///:~
```

<!--p800-->
The output is identical to the previous DBTable example. The processor and the visitor are inner classes in this example. Note that the process( ) method only adds the visitor class and initializes the SQL string. Both parameters of getDeclarationScanner( ) are visitors; the first is used before each declaration is visited and the second is used afterwards. This processor only needs the pre- visit visitor, so NO_OP is given as the second parameter. This is a static field in the DeclarationVisitor interface, which is a DeclarationVisitor that doesn’t do anything. TableCreationVisitor extends SimpleDeclarationVisitor, overriding the two methods visitClassDeclaration( ) and visitFieldDeclaration( ). The Annotations SimpleDeclarationVisitor is an adapter that implements all of the methods on the Declaration Visitor interface, so you can concentrate on the ones you need. In visitClassDeclaration( ), the ClassDeclaration object is checked for the DBTable annotation, and if it is there, the first part of the SQL creation String is initialized. In visitFieldDeclaration( ), the field declaration is queried for its field annotations and the information is extracted in much the same way as it was in the original example, earlier in the chapter. This may seem like a more complicated way of doing things, but it produces a more scalable solution. If the complexity of your annotation processor increases, then writing your own standalone processor as in the earlier example would soon become quite complicated. Exercise 3:(2) Add support for more SQL types to TableCreationProcessorFactory.java. Annotation-based unit testing Unit testing is the practice of creating one or more tests for each method in a class, in order to regularly test the portions of a class for correct behavior. The most popular tool used for unit testing in Java is called JUnit; at the time of this writing, JUnit was in the process of being updated to JUnit version 4, in order to incorporate annotations.6One of the main problems with preannotation versions of JUnit is the amount of "ceremony" necessary in order to set up and run JUnit tests. This has been reduced over time, but annotations will move testing closer to "the simplest unit testing system that can possibly work." With pre-annotation versions of JUnit, you must create a separate class to hold your unit tests. With annotations we can include the unit tests inside the class to be tested, and thus reduce the time and trouble of unit testing to a minimum. This approach has the additional benefit of being able to test private methods as easily as public ones. Since this example test framework is annotation-based, it’s called @Unit. The most basic form of testing, and one which you will probably use much of the time, only needs the @Test annotation to indicate which methods should be tested. One option is for the test methods to take no arguments and return a boolean to indicate success or failure. You can use any name you like for test methods. Also, @Unit test methods can have any access that you’d like, including private. To use @Unit, all you need to do is import net.mindview.atunit,7mark the appropriate methods and fields with @Unit test tags (which you’ll learn about in the following examples) and then have your build system run @Unit on the resulting class. Here’s a simple example:
```java
//: annotations/AtUnitExample1.java
package annotations;
import net.mindview.atunit.*;
import net.mindview.util.*;
public class AtUnitExample1 {
public String methodOne() {
return "This is methodOne";
}
public int methodTwo() {
System.out.println("This is methodTwo");
return 2;
```

<!--p801-->
6 I originally had thoughts of making a "better JUnit" based on the design shown here. However, it appears that JUnit4 also includes many of the ideas presented here, so it remains easier to go along with that. 7 This library is part of this book’s code package, available at www.MindView.net.
```java
}
@Test boolean methodOneTest() {
return methodOne().equals("This is methodOne");
}
@Test boolean m2() { return methodTwo() == 2; }
@Test private boolean m3() { return true; }
// Shows output for failure:
@Test boolean failureTest() { return false; }
@Test boolean anotherDisappointment() { return false; }
public static void main(String[] args) throws Exception {
OSExecute.command(
"java net.mindview.atunit.AtUnit AtUnitExample1");
}
} /* Output:
annotations.AtUnitExample1
. methodOneTest
. m2 This is methodTwo
. m3
. failureTest (failed)
. anotherDisappointment (failed)
(5 tests)
>>> 2 FAILURES <<<
annotations.AtUnitExample1: failureTest
annotations.AtUnitExample1: anotherDisappointment
*///:~
```
Classes to be @Unit tested must be placed in packages. The @Test annotation preceding the methods methodOneTest( ), m2( ), m3( ), failureTest( ) and anotherDisappointment( ) tells @Unit to run these methods as unit tests. It will also ensure that those methods take no arguments and return a boolean or void. Your only responsibility when you write the unit test is to determine whether the test succeeds or fails and returns true or false, respectively (for methods that return boolean). If you’re familiar with JUnit, you’ll also note @Unit’s more informative output—you can see the test that’s currently being run so the output from that test is more useful, and at the end it tells you the classes and tests that caused failures. You’re not forced to embed test methods inside your classes, if that doesn’t work for you. The easiest way to create non-embedded tests is with inheritance:
```java
//: annotations/AtUnitExternalTest.java
// Creating non-embedded tests.
package annotations;
import net.mindview.atunit.*;
import net.mindview.util.*;
public class AtUnitExternalTest extends AtUnitExample1 {
@Test boolean _methodOne() {
return methodOne().equals("This is methodOne");
}
@Test boolean _methodTwo() { return methodTwo() == 2; }
public static void main(String[] args) throws Exception {
OSExecute.command(
"java net.mindview.atunit.AtUnit AtUnitExternalTest");
}
} /* Output:
annotations.AtUnitExternalTest
. _methodOne
```

<!--p802-->
Annotations
```java
. _methodTwo This is methodTwo
OK (2 tests)
*///:~
```
This example also demonstrates the value of flexible naming (in contrast to JUnit’s requirement to start all your tests with the word "test"). Here, @Test methods that are directly testing another method are given the name of that method starting with an underscore (I’m not suggesting that this is an ideal style, just showing a possibility). You can also use composition to create non-embedded tests:
```java
//: annotations/AtUnitComposition.java
// Creating non-embedded tests.
package annotations;
import net.mindview.atunit.*;
import net.mindview.util.*;
public class AtUnitComposition {
AtUnitExample1 testObject = new AtUnitExample1();
@Test boolean _methodOne() {
return
testObject.methodOne().equals("This is methodOne");
}
@Test boolean _methodTwo() {
return testObject.methodTwo() == 2;
}
public static void main(String[] args) throws Exception {
OSExecute.command(
"java net.mindview.atunit.AtUnit AtUnitComposition");
}
} /* Output:
annotations.AtUnitComposition
. _methodOne
. _methodTwo This is methodTwo
OK (2 tests)
*///:~
```
A new member testObject is created for each test, since an AtUnitComposition object is created for each test. There are no special "assert" methods as there are in JUnit, but the second form of the @Test method allows you to return void (or boolean, if you still want to return true or false in this case). To test for success, you can use Java assert statements. Java assertions normally have to be enabled with the -ea flag on the java command line, but @Unit automatically enables them. To indicate failure, you can even use an exception. One of the @Unit design goals is to require as little additional syntax as possible, and Java’s assert and exceptions are all that is necessary to report errors. A failed assert or an exception that emerges from the test method is treated as a failed test, but @Unit does not halt in this case—it continues until all the tests are run. Here’s an example:

<!--p803-->
```java
//: annotations/AtUnitExample2.java
// Assertions and exceptions can be used in @Tests.
package annotations;
import java.io.*;
import net.mindview.atunit.*;
import net.mindview.util.*;
public class AtUnitExample2 {
public String methodOne() {
return "This is methodOne";
}
public int methodTwo() {
System.out.println("This is methodTwo");
return 2;
}
@Test void assertExample() {
assert methodOne().equals("This is methodOne");
}
@Test void assertFailureExample() {
assert 1 == 2: "What a surprise!";
}
@Test void exceptionExample() throws IOException {
new FileInputStream("nofile.txt"); // Throws
}
@Test boolean assertAndReturn() {
// Assertion with message:
assert methodTwo() == 2: "methodTwo must equal 2";
return methodOne().equals("This is methodOne");
}
public static void main(String[] args) throws Exception {
OSExecute.command(
"java net.mindview.atunit.AtUnit AtUnitExample2");
}
} /* Output:
annotations.AtUnitExample2
. assertExample
. assertFailureExample java.lang.AssertionError: What a surprise!
(failed)
. exceptionExample java.io.FileNotFoundException: nofile.txt (The
system cannot find the file specified)
(failed)
. assertAndReturn This is methodTwo
(4 tests)
>>> 2 FAILURES <<<
annotations.AtUnitExample2: assertFailureExample
annotations.AtUnitExample2: exceptionExample
*///:~
```
Here’s an example using non-embedded tests with assertions, performing some simple tests of java.util.HashSet:
```java
//: annotations/HashSetTest.java
package annotations;
import java.util.*;
import net.mindview.atunit.*;
import net.mindview.util.*;
public class HashSetTest {
HashSet<String> testObject = new HashSet<String>();
@Test void initialization() {
assert testObject.isEmpty();
}
@Test void _contains() {
testObject.add("one");
assert testObject.contains("one");
}
@Test void _remove() {
testObject.add("one");
testObject.remove("one");
```

<!--p804-->
Annotations
```java
assert testObject.isEmpty();
}
public static void main(String[] args) throws Exception {
OSExecute.command(
"java net.mindview.atunit.AtUnit HashSetTest");
}
} /* Output:
annotations.HashSetTest
. initialization
. _remove
. _contains
OK (3 tests)
*///:~
```
The inheritance approach would seem to be simpler, in the absence of other constraints. Exercise 4:(3) Verify that a new testObject is created before each test. Exercise 5:(1) Modify the above example to use the inheritance approach. Exercise 6:(1) Test LinkedList using the approach shown in HashSetTest.j ava. Exercise 7:(1) Modify the previous exercise to use the inheritance approach. For each unit test, @Unit creates an object of the class under test using the default constructor. The test is called for that object, and then the object is discarded to prevent side effects from leaking into other unit tests. This relies on the default constructor to create the objects. If you don’t have a default constructor or you need more sophisticated construction for objects, you create a static method to build the object and attach the @TestObjectCreate annotation, like this:

<!--p805-->
```java
//: annotations/AtUnitExample3.java
package annotations;
import net.mindview.atunit.*;
import net.mindview.util.*;
public class AtUnitExample3 {
private int n;
public AtUnitExample3(int n) { this.n = n; }
public int getN() { return n; }
public String methodOne() {
return "This is methodOne";
}
public int methodTwo() {
System.out.println("This is methodTwo");
return 2;
}
@TestObjectCreate static AtUnitExample3 create() {
return new AtUnitExample3(47);
}
@Test boolean initialization() { return n == 47; }
@Test boolean methodOneTest() {
return methodOne().equals("This is methodOne");
}
@Test boolean m2() { return methodTwo() == 2; }
public static void main(String[] args) throws Exception {
OSExecute.command(
"java net.mindview.atunit.AtUnit AtUnitExample3");
}
} /* Output:
annotations.AtUnitExample3
. initialization
. methodOneTest
. m2 This is methodTwo
OK (3 tests)
*///:~
```
The @TestObjectCreate method must be static and must return an object of the type that you’re testing—the @Unit program will ensure that this is true. Sometimes you need additional fields to support your unit testing. The @TestProperty annotation can be used to tag fields that are only used for unit testing (so that they can be removed before you deliver the product to the client). Here’s an example that reads values from a String that is broken up using the String.split( ) method. This input is used to produce test objects:
```java
//: annotations/AtUnitExample4.java
package annotations;
import java.util.*;
import net.mindview.atunit.*;
import net.mindview.util.*;
import static net.mindview.util.Print.*;
public class AtUnitExample4 {
static String theory = "All brontosauruses " +
"are thin at one end, much MUCH thicker in the " +
"middle, and then thin again at the far end.";
private String word;
private Random rand = new Random(); // Time-based seed
public AtUnitExample4(String word) { this.word = word; }
public String getWord() { return word; }
public String scrambleWord() {
List<Character> chars = new ArrayList<Character>();
for(Character c : word.toCharArray())
chars.add(c);
Collections.shuffle(chars, rand);
StringBuilder result = new StringBuilder();
for(char ch : chars)
result.append(ch);
return result.toString();
}
@TestProperty static List<String> input =
Arrays.asList(theory.split(" "));
@TestProperty
static Iterator<String> words = input.iterator();
@TestObjectCreate static AtUnitExample4 create() {
if(words.hasNext())
return new AtUnitExample4(words.next());
else
return null;
}
@Test boolean words() {
print("‘" + getWord() + "‘");
return getWord().equals("are");
}
@Test boolean scramble1() {
// Change to a specific seed to get verifiable results:
rand = new Random(47);
print("‘" + getWord() + "‘");
String scrambled = scrambleWord();
print(scrambled);
```

<!--p806-->
Annotations
```java
return scrambled.equals("lAl");
}
@Test boolean scramble2() {
rand = new Random(74);
print("‘" + getWord() + "‘");
String scrambled = scrambleWord();
print(scrambled);
return scrambled.equals("tsaeborornussu");
}
public static void main(String[] args) throws Exception {
System.out.println("starting");
OSExecute.command(
"java net.mindview.atunit.AtUnit AtUnitExample4");
}
} /* Output:
starting
annotations.AtUnitExample4
. scramble1 ‘All’
lAl
. scramble2 ‘brontosauruses’
tsaeborornussu
. words ‘are’
OK (3 tests)
*///:~
```
@TestProperty can also be used to tag methods that may be used during testing, but are not tests themselves. Note that this program relies on the execution order of the tests, which is in general not a good practice. If your test object creation performs initialization that requires later cleanup, you can optionally add a static @TestObjectCleanup method to perform cleanup when you are finished with the test object. In this example, @TestObjectCreate opens a file to create each test object, so the file must be closed before the test object is discarded:

<!--p807-->
```java
//: annotations/AtUnitExample5.java
package annotations;
import java.io.*;
import net.mindview.atunit.*;
import net.mindview.util.*;
public class AtUnitExample5 {
private String text;
public AtUnitExample5(String text) { this.text = text; }
public String toString() { return text; }
@TestProperty static PrintWriter output;
@TestProperty static int counter;
@TestObjectCreate static AtUnitExample5 create() {
String id = Integer.toString(counter++);
try {
output = new PrintWriter("Test" + id + ".txt");
} catch(IOException e) {
throw new RuntimeException(e);
}
return new AtUnitExample5(id);
}
@TestObjectCleanup static void
cleanup(AtUnitExample5 tobj) {
System.out.println("Running cleanup");
output.close();
}
@Test boolean test1() {
output.print("test1");
return true;
}
@Test boolean test2() {
output.print("test2");
return true;
}
@Test boolean test3() {
output.print("test3");
return true;
}
public static void main(String[] args) throws Exception {
OSExecute.command(
"java net.mindview.atunit.AtUnit AtUnitExample5");
}
} /* Output:
annotations.AtUnitExample5
. test1
Running cleanup
. test2
Running cleanup
. test3
Running cleanup
OK (3 tests)
*///:~
```
You can see from the output that the cleanup method is automatically run after each test.
## Using @Unit with generics
Generics pose a special problem, because you can’t "test generically." You must test for a specific type parameter or set of parameters. The solution is simple: Inherit a test class from a specified version of the generic class. Here’s a simple implementation of a stack:
```java
//: annotations/StackL.java
// A stack built on a linkedList.
package annotations;
import java.util.*;
public class StackL<T> {
private LinkedList<T> list = new LinkedList<T>();
public void push(T v) { list.addFirst(v); }
public T top() { return list.getFirst(); }
public T pop() { return list.removeFirst(); }
} ///:~
```
To test a String version, inherit a test class from StackL<String>:
```java
//: annotations/StackLStringTest.java
// Applying @Unit to generics.
package annotations;
import net.mindview.atunit.*;
import net.mindview.util.*;
```

<!--p808-->
Annotations
```java
public class StackLStringTest extends StackL<String> {
@Test void _push() {
push("one");
assert top().equals("one");
push("two");
assert top().equals("two");
}
@Test void _pop() {
push("one");
push("two");
assert pop().equals("two");
assert pop().equals("one");
}
@Test void _top() {
push("A");
push("B");
assert top().equals("B");
assert top().equals("B");
}
public static void main(String[] args) throws Exception {
OSExecute.command(
"java net.mindview.atunit.AtUnit StackLStringTest");
}
} /* Output:
annotations.StackLStringTest
. _push
. _pop
. _top
OK (3 tests)
*///:~
```

<!--p809-->
The only potential drawback to inheritance is that you lose the ability to access private methods in the class under test. If this is a problem, you can either make the method in question protected, or add a non-private @TestProperty method that calls the private method (the @TestProperty method will then be stripped out of the production code by the AtUnitRemover tool that is shown later in this chapter). Exercise 8:(2) Create a class with a private method and add a non-private @TestProperty method as described above. Call this method in your test code. Exercise 9:(2) Write basic @Unit tests for HashMap. Exercise 10:(2) Select an example from elsewhere in the book and add @Unit tests. No “suites” necessary One of the big advantages of @Unit over JUnit is that "suites" are unnecessary. In JUnit, you need to somehow tell the unit testing tool what it is that you need to test, and this requires the introduction of "suites" to group tests together so that JUnit can find them and run the tests. @Unit simply searches for class files containing the appropriate annotations, and then executes the @Test methods. Much of my goal with the @Unit testing system is to make it incredibly transparent, so that people can begin using it by simply adding @Test methods, with no other special code or knowledge like that required by JUnit and many other unit testing frameworks. It’s hard enough to write tests without adding any new hurdles, so @Unit tries to make it trivial. This way, you’re more likely to actually write the tests.
## Implementing @Unit
First, we need to define all the annotation types. These are simple tags, and have no fields. The @Test tag was defined at the beginning of the chapter, and here are the rest of the annotations:
```java
//: net/mindview/atunit/TestObjectCreate.java
// The @Unit @TestObjectCreate tag.
package net.mindview.atunit;
import java.lang.annotation.*;
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface TestObjectCreate {} ///:~
//: net/mindview/atunit/TestObjectCleanup.java
// The @Unit @TestObjectCleanup tag.
package net.mindview.atunit;
import java.lang.annotation.*;
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface TestObjectCleanup {} ///:~
//: net/mindview/atunit/TestProperty.java
// The @Unit @TestProperty tag.
package net.mindview.atunit;
import java.lang.annotation.*;
// Both fields and methods may be tagged as properties:
@Target({ElementType.FIELD, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
public @interface TestProperty {} ///:~
```
All the tests have RUNTIME retention because the @Unit system must discover the tests in compiled code. To implement the system that runs the tests, we use reflection to extract the annotations. The program uses this information to decide how to build the test objects and run tests on them. Because of annotations this is surprisingly small and straightforward:
```java
//: net/mindview/atunit/AtUnit.java
// An annotation-based unit-test framework.
// {RunByHand}
package net.mindview.atunit;
import java.lang.reflect.*;
import java.io.*;
import java.util.*;
import net.mindview.util.*;
import static net.mindview.util.Print.*;
public class AtUnit implements ProcessFiles.Strategy {
static Class<?> testClass;
static List<String> failedTests= new ArrayList<String>();
static long testsRun = 0;
static long failures = 0;
public static void main(String[] args) throws Exception {
ClassLoader.getSystemClassLoader()
.setDefaultAssertionStatus(true); // Enable asserts
new ProcessFiles(new AtUnit(), "class").start(args);
```

<!--p810-->
Annotations

<!--p811-->
```java
if(failures == 0)
print("OK (" + testsRun + " tests)");
else {
print("(" + testsRun + " tests)");
print("\n>>> " + failures + " FAILURE" +
(failures > 1 ? "S" : "") + " <<<");
for(String failed : failedTests)
print(" " + failed);
}
}
public void process(File cFile) {
try {
String cName = ClassNameFinder.thisClass(
BinaryFile.read(cFile));
if(!cName.contains("."))
return; // Ignore unpackaged classes
testClass = Class.forName(cName);
} catch(Exception e) {
throw new RuntimeException(e);
}
TestMethods testMethods = new TestMethods();
Method creator = null;
Method cleanup = null;
for(Method m : testClass.getDeclaredMethods()) {
testMethods.addIfTestMethod(m);
if(creator == null)
creator = checkForCreatorMethod(m);
if(cleanup == null)
cleanup = checkForCleanupMethod(m);
}
if(testMethods.size() > 0) {
if(creator == null)
try {
if(!Modifier.isPublic(testClass
.getDeclaredConstructor().getModifiers())) {
print("Error: " + testClass +
" default constructor must be public");
System.exit(1);
}
} catch(NoSuchMethodException e) {
// Synthesized default constructor; OK
}
print(testClass.getName());
}
for(Method m : testMethods) {
printnb(" . " + m.getName() + " ");
try {
Object testObject = createTestObject(creator);
boolean success = false;
try {
if(m.getReturnType().equals(boolean.class))
success = (Boolean)m.invoke(testObject);
else {
m.invoke(testObject);
success = true; // If no assert fails
}
} catch(InvocationTargetException e) {
// Actual exception is inside e:
print(e.getCause());
}
print(success ? "" : "(failed)");
testsRun++;
if(!success) {
failures++;
failedTests.add(testClass.getName() +
": " + m.getName());
}
if(cleanup != null)
cleanup.invoke(testObject, testObject);
} catch(Exception e) {
throw new RuntimeException(e);
}
}
}
static class TestMethods extends ArrayList<Method> {
void addIfTestMethod(Method m) {
if(m.getAnnotation(Test.class) == null)
return;
if(!(m.getReturnType().equals(boolean.class) ||
m.getReturnType().equals(void.class)))
throw new RuntimeException("@Test method" +
" must return boolean or void");
m.setAccessible(true); // In case it’s private, etc.
add(m);
}
}
private static Method checkForCreatorMethod(Method m) {
if(m.getAnnotation(TestObjectCreate.class) == null)
return null;
if(!m.getReturnType().equals(testClass))
throw new RuntimeException("@TestObjectCreate " +
"must return instance of Class to be tested");
if((m.getModifiers() &
java.lang.reflect.Modifier.STATIC) < 1)
throw new RuntimeException("@TestObjectCreate " +
"must be static.");
m.setAccessible(true);
return m;
}
private static Method checkForCleanupMethod(Method m) {
if(m.getAnnotation(TestObjectCleanup.class) == null)
return null;
if(!m.getReturnType().equals(void.class))
throw new RuntimeException("@TestObjectCleanup " +
"must return void");
if((m.getModifiers() &
java.lang.reflect.Modifier.STATIC) < 1)
throw new RuntimeException("@TestObjectCleanup " +
"must be static.");
if(m.getParameterTypes().length == 0 ||
m.getParameterTypes()[0] != testClass)
throw new RuntimeException("@TestObjectCleanup " +
"must take an argument of the tested type.");
m.setAccessible(true);
return m;
}
private static Object createTestObject(Method creator) {
if(creator != null) {
try {
return creator.invoke(testClass);
} catch(Exception e) {
throw new RuntimeException("Couldn’t run " +
"@TestObject (creator) method.");
}
} else { // Use the default constructor:
try {
```

<!--p812-->
Annotations
```java
return testClass.newInstance();
} catch(Exception e) {
throw new RuntimeException("Couldn’t create a " +
"test object. Try using a @TestObject method.");
}
}
}
} ///:~
```
AtUnit.java uses the ProcessFiles tool in net.mindview.util. The AtUnit class implements ProcessFiles.Strategy, which comprises the method process( ). This way, an instance of AtUnit can be passed to the ProcessFiles constructor. The second constructor argument tells ProcessFiles to look for all files that have "class" extensions. If you do not provide a command-line argument, the program will traverse the current directory tree. You may also provide multiple arguments which can be either class files (with or without the .class extension) or directories. Since @Unit will automatically find the testable classes and methods, no "suite" mechanism is necessary.8 One of the problems that AtUnit.java must solve when it discovers class files is that the actual qualified class name (including package) is not evident from the class file name. In order to discover this information, the class file must be analyzed, which is not trivial, but not impossible, either.9 So the first thing that happens when a .class file is found is that it is opened and its binary data is read and handed to ClassNameFinder.thisClass( ). Here, we are moving into the realm of "bytecode engineering," because we are actually analyzing the contents of a class file:
```java
//: net/mindview/atunit/ClassNameFinder.java
package net.mindview.atunit;
import java.io.*;
import java.util.*;
import net.mindview.util.*;
import static net.mindview.util.Print.*;
public class ClassNameFinder {
public static String thisClass(byte[] classBytes) {
Map<Integer,Integer> offsetTable =
new HashMap<Integer,Integer>();
Map<Integer,String> classNameTable =
new HashMap<Integer,String>();
try {
DataInputStream data = new DataInputStream(
new ByteArrayInputStream(classBytes));
int magic = data.readInt(); // 0xcafebabe
int minorVersion = data.readShort();
int majorVersion = data.readShort();
int constant_pool_count = data.readShort();
int[] constant_pool = new int[constant_pool_count];
for(int i = 1; i < constant_pool_count; i++) {
int tag = data.read();
int tableSize;
switch(tag) {
case 1: // UTF
int length = data.readShort();
char[] bytes = new char[length];
for(int k = 0; k < bytes.length; k++)
bytes[k] = (char)data.read();
```

<!--p813-->
8 It is not clear why the default constructor for the class under test must be public, but if it isn’t, the call to newlnstance( ) just hangs (doesn’t throw an exception). 9 Jeremy Meyer and I spent most of a day figuring this out. Annotations
```java
String className = new String(bytes);
classNameTable.put(i, className);
break;
case 5: // LONG
case 6: // DOUBLE
data.readLong(); // discard 8 bytes
i++; // Special skip necessary
break;
case 7: // CLASS
int offset = data.readShort();
offsetTable.put(i, offset);
break;
case 8: // STRING
data.readShort(); // discard 2 bytes
break;
case 3: // INTEGER
case 4: // FLOAT
case 9: // FIELD_REF
case 10: // METHOD_REF
case 11: // INTERFACE_METHOD_REF
case 12: // NAME_AND_TYPE
data.readInt(); // discard 4 bytes;
break;
default:
throw new RuntimeException("Bad tag " + tag);
}
}
short access_flags = data.readShort();
int this_class = data.readShort();
int super_class = data.readShort();
return classNameTable.get(
offsetTable.get(this_class)).replace(‘/’, ‘.’);
} catch(Exception e) {
throw new RuntimeException(e);
}
}
// Demonstration:
public static void main(String[] args) throws Exception {
if(args.length > 0) {
for(String arg : args)
print(thisClass(BinaryFile.read(new File(arg))));
} else
// Walk the entire tree:
for(File klass : Directory.walk(".", ".*\\.class"))
print(thisClass(BinaryFile.read(klass)));
}
} ///:~
```

<!--p814-->
Although it’s not possible to go into full detail here, each class file follows a particular format and I’ve tried to use meaningful field names for the pieces of data that are picked out of the ByteArraylnputStream; you can also see the size of each piece by the length of the read performed on the input stream. For example, the first 32 bits of any class file is always the "magic number" hex 0xcafebabe,10and the next two shorts are version information. The constant pool contains the constants for the program and so is of variable size; the next short tells how big it is, so that an appropriate-sized array can be allocated. Each entry in the constant pool may be a fixed-size or variablesized value, so we must examine the tag that begins each one to find out what to do with it—that’s the switch statement. Here, we are not trying to accurately analyze all the data in the class file, but merely to step through and store the pieces of interest, so you’ll notice that a fair amount of data is discarded. Information 10 Various legends surround the meaning of this, but since Java was created by nerds we can make a reasonable guess that it had something to do with fantasizing about a woman in a coffee shop. about classes is stored in the classNameTable and the offsetTable. After the constant pool is read, the this_class information can be found, which is an index into the offsetTable, which produces an index into the classNameTable, which produces the class name. Back in AtUnit.java, process( ) now has the class name and can look to see if it contains a ‘.’, which means it’s in a package. Unpackaged classes are ignored. If a class is in a package, the standard class loader is used to load the class with Class.forName( ). Now the class can be analyzed for @Unit annotations. We only need to look for three things: @Test methods, which are stored in a TestMethods list, and whether there’s an @TestObjectCreate and @TestObjectCleanup method. These are discovered through the associated method calls that you see in the code, which look for the annotations. If any @Test methods have been found, the name of the class is printed so the viewer can see what’s happening, and then each test is executed. This means printing the method name, then calling createTestObject( ), which will use the @TestObjectCreate method if one exists, or will fall back to the default constructor otherwise. Once the test object has been created, the test method is invoked upon that object. If the test returns a boolean, the result is captured. If not, we assume success if there is no exception (which would happen in the case of a failed assert or any other kind of exception). If an exception is thrown, the exception information is printed to show the cause. If any failure occurs, the failure count is increased and the class name and method are added to failedTests so these can be reported at the end of the run. Exercise 11: (5) Add an @TestNote annotation to @Unit, so that the accompanying note is simply displayed during testing. Removing test code Although in many projects it won’t make a difference if you leave the test code in the deliverable (especially if you make all the test methods private, which you can do if you like), in some cases you will want to strip out the test code either to keep the deliverable small or so that it is not exposed to the client. This requires more sophisticated bytecode engineering than it is comfortable to do by hand. However, the open-source Javassist library11brings bytecode engineering into the realm of the possible. The following program takes an optional -r flag as its first argument; if you provide the flag it will remove the @Test annotations, and if you do not it will simply display the @Test annotations. ProcessFiles is also used here to traverse the files and directories of your choosing:
```java
//: net/mindview/atunit/AtUnitRemover.java
// Displays @Unit annotations in compiled class files. If
// first argument is "-r", @Unit annotations are removed.
// {Args: ..}
// {Requires: javassist.bytecode.ClassFile;
// You must install the Javassist library from
// http://sourceforge.net/projects/jboss/ }
package net.mindview.atunit;
import javassist.*;
import javassist.expr.*;
import javassist.bytecode.*;
import javassist.bytecode.annotation.*;
```

<!--p815-->
11 Thanks to Dr. Shigeru Chiba for creating this library, and for all his help in developing AtUnitRemover.java.
```java
import java.io.*;
import java.util.*;
import net.mindview.util.*;
import static net.mindview.util.Print.*;
public class AtUnitRemover
implements ProcessFiles.Strategy {
private static boolean remove = false;
public static void main(String[] args) throws Exception {
if(args.length > 0 && args[0].equals("-r")) {
remove = true;
String[] nargs = new String[args.length - 1];
System.arraycopy(args, 1, nargs, 0, nargs.length);
args = nargs;
}
new ProcessFiles(
new AtUnitRemover(), "class").start(args);
}
public void process(File cFile) {
boolean modified = false;
try {
String cName = ClassNameFinder.thisClass(
BinaryFile.read(cFile));
if(!cName.contains("."))
return; // Ignore unpackaged classes
ClassPool cPool = ClassPool.getDefault();
CtClass ctClass = cPool.get(cName);
for(CtMethod method : ctClass.getDeclaredMethods()) {
MethodInfo mi = method.getMethodInfo();
AnnotationsAttribute attr = (AnnotationsAttribute)
mi.getAttribute(AnnotationsAttribute.visibleTag);
if(attr == null) continue;
for(Annotation ann : attr.getAnnotations()) {
if(ann.getTypeName()
.startsWith("net.mindview.atunit")) {
print(ctClass.getName() + " Method: "
+ mi.getName() + " " + ann);
if(remove) {
ctClass.removeMethod(method);
modified = true;
}
}
}
}
// Fields are not removed in this version (see text).
if(modified)
ctClass.toBytecode(new DataOutputStream(
new FileOutputStream(cFile)));
ctClass.detach();
} catch(Exception e) {
throw new RuntimeException(e);
}
}
} ///:~
```

<!--p816-->

<!--p817-->
The ClassPool is a kind of picture of all the classes in the system that you are modifying. It guarantees the consistency of all the modified classes. You must get each CtClass from the ClassPool, similar to the way the class loader and Class.forName( ) load classes into the JVM. The CtClass contains the bytecodes for a class object and allows you to produce information about the class and to manipulate the code in the class. Here, we call Annotations getDeclaredMethods( ) (just like Java’s reflection mechanism) and get a MethodInfo object from each CtMethod object. From this, we can look at the annotations. If a method has an annotation in the net.mindview.atunit package, that method is removed. If the class has been modified, the original class file is overwritten with the new class. At the time of this writing, the "remove" functionality in Javassist had recently been added,12 and we discovered that removing @TestProperty fields turns out to be more complex than removing methods. Because there may be static initialization operations that refer to those fields, you cannot simply remove them. So the above version of the code only removes @Unit methods. However, you should check the Javassist Web site for updates; field removal should eventually be possible. In the meantime, note that the external testing method shown in AtUnitExternalTest.java allows all tests to be removed by simply deleting the class file created by the test code. 12 Dr. Shigeru Chiba very nicely added the CtClass.removeMethod( ) at our request. Annotations Summary Annotations are a welcome addition to Java. They are a structured and typechecked means of adding metadata to your code without rendering it unreadable and messy. They can help remove the tedium of writing deployment descriptors and other generated files. The fact that the @deprecated Javadoc tag has been superseded by the @Deprecated annotation is just one indication of how much better suited annotations are for describing information about classes than are comments. Only a small handful of annotations come with Java SE5. This means that, if you can’t find a library elsewhere, you will be creating annotations and the associated logic to do this. With the apt tool, you can compile newly generated files in one step, easing the build process, but currently there is little more in the mirror API than some basic functionality to help you identify the elements of Java class definitions. As you’ve seen, Javassist can be used for bytecode engineering, or you can hand-code your own bytecode manipulation tools. This situation will certainly improve, and providers of APIs and frameworks will start providing annotations as part of their toolkits. As you can imagine by seeing the @Unit system, it is very likely that annotations will cause significant changes in our Java programming experience. Solutions to selected exercises can be found in the electronic document The Thinking in Java Annotated Solution Guide, available for sale from www.MindView.net.