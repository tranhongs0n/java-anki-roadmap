---
cardId: 1795706077204
cardKey: jv-0001-a1c5abdb2f
deck: 00 Java Roadmap::01 Foundations::02 Basic Syntax
flag: 1
created: 2026-11-27
status: done
sources:
  - https://dev.java/learn/language/constructs/basics/arrays/
  - https://docs.oracle.com/javase/specs/jls/se21/html/jls-4.html#jls-4.12.5
tags:
  - java
  - arrays
---

# 2-D array trong Java: mảng của các mảng

## Thẻ gốc

> **Front:** How does a Java 2-D array differ from a C or Fortran 2-D array?
> **Back:** It is not one contiguous memory block, so rows may vary in length

## Giải thích

Điểm cần nhớ: trong Java không có "ma trận" như một khối bộ nhớ. `int[][]` đọc đúng theo nghĩa đen là **mảng của các mảng**.

Ba tầng của câu chuyện:

1. **Mảng ngoài** (`grid`) là một object, các phần tử của nó liên tiếp nhau trong bộ nhớ, nhưng mỗi phần tử là một *con trỏ* (reference) tới một mảng hàng, không phải số nguyên.
2. **Mỗi hàng** (`grid[0]`, `grid[1]`, …) là một object mảng riêng, cấp phát riêng, có thể nằm ở chỗ khác trong heap.
3. Vì vậy **không có gì bắt các hàng phải bằng nhau**. Hàng dài 1, hàng dài 2, hàng dài 3 là hợp lệ — đó là *jagged* (irregular) array, và đây chính là điều dev.java nêu khi so với C/Fortran.

Trong C, `int a[3][4]` là 12 `int` liền nhau; địa chỉ của `a[i][j]` tính bằng số học con trỏ trên một khối duy nhất. Trong Java, `grid[i][j]` là hai lần dereference: lấy reference ở hàng `i`, rồi lấy phần tử `j` của mảng đó. Chi phí và ngữ nghĩa khác nhau, và cũng vì thế Java kiểm tra biên từng chiều riêng.

Hệ quả thực dụng:

```java
int[][] grid = new int[3][];      // chỉ mảng ngoài tồn tại: 3 slot null
grid[0] = new int[1];             // hàng tam giác
grid[1] = new int[2];
grid[2] = new int[3];
grid[1][0] = 42;                  // ok
// grid[0][0] trước khi có new int[1] -> NullPointerException
```

`new int[3][]` cấp phát mảng ngoài, không cấp phát hàng nào. Mặc định của phần tử reference là `null` (JLS §4.12.5), nên chạm vào `grid[0][0]` trước khi cấp hàng là NPE — lỗi rất hay gặp và không phải `ArrayIndexOutOfBoundsException`.

Với người chuyển từ OutSystems: `List of Record` bên đó là một danh sách động, tự lớn, còn `grid` ở đây là cấu trúc cố định sau khi `new` — không `add()` được. Muốn co giãn thì dùng `List<List<Integer>>` hoặc `ArrayList<int[]>`, và mỗi hàng vẫn là một object riêng.

## Facts đã kiểm

- [x] "a multidimensional array is an array whose components are themselves arrays" — dev.java, Creating Multidimensional Arrays
- [x] "in Java an array is a contiguous zone of memory, but as a bidimensional array is an array of references, it is not itself a contiguous zone of memory" — dev.java
- [x] "the rows are allowed to vary in length"; "These arrays are sometimes called irregular arrays, or jagged arrays" — dev.java
- [x] "For all reference types, the default value is null" — JLS SE 21 §4.12.5

## Thẻ sinh ra

- `jv-0001-7ab005f3cb` — Is a Java 2-D array one contiguous block of memory like a C or Fortran matrix?
- `jv-0001-4affaf10b2` — May the rows of a Java 2-D array have different lengths?
- `jv-0001-19f0c5f201` — After `int[][] grid = new int[3][];`, what does `grid[0]` hold?

## Ghi chú

Thẻ gốc giữ nguyên, không sửa; nội dung nó đã đúng, chỉ thiếu chỗ để hiểu *vì sao*. Batch: `cards/arrays-2d.json`.
