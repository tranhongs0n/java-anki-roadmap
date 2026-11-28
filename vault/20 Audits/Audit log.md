# Audit log

Mỗi mục: thẻ, phán quyết, lý do, hành động đã làm. Flag 2 là hàng đợi audit; flag 1 là hàng đợi giải thích.

## 2026-11-27

### Card 1795706077222 — deleted

**Card:** A loop counts letter 'p' by iterating characters; what happens if the `continue` is removed?
**Back:** The count becomes wrong, counting every character

Phán quyết: **delete** (không rewrite).

- Front tham chiếu một đoạn code chỉ có trong bài viết, không có trên thẻ — người học không thể dựng lại tình huống.
- Extra bị hỏng văn bản: "The original 9 'p's become 35 's example." — câu đứt giữa, không truyền đạt được gì.
- Sự kiện bên dưới ("continue bỏ phần còn lại của vòng lặp hiện tại") đã có 3 thẻ phủ: 1795706077221, 1795752249864, và hai thẻ break-vs-continue.
- Kiểu "chuyện gì xảy ra nếu xoá dòng này" chỉ kiểm tra một ví dụ cụ thể, không phải một quy tắc dùng lại được.

Hành động: xoá note khỏi Anki, xoá entry khỏi `cards/devjava-CHUNK-0.json` (đã verify `notesInfo` trả về rỗng, 0 card còn lại).

### Hàng đợi mở

- 1795706077234 + 1795706077233 — cùng một sự kiện (selector của switch), một khẳng định một phủ định; đề xuất gộp thành một thẻ bullet và xoá thẻ phủ định. Chờ quyết định.
- 1795750484756 "What does break do versus continue?" và 1795745004671 "What is the difference between break and continue?" — trùng nghĩa, giữ một.

### Subagent review — 3 cards flagged during example backfill (2026-11-28)

- `jv-0005-7f66c8a982` "When does findFirst() have to process every element?" — **giữ nguyên**. Subagent nghi ngờ, nhưng thẻ đúng: với stream rỗng, findFirst() phải đi hết pipeline để chứng minh không có phần tử, rồi trả Optional.empty().
- `jv-0005-5e8579bbb8` "What breaks when you fill a list with stream.forEach(result::add)?" — **sửa Back**. Back cũ nói side effect "blocks parallel execution" (sai: nó không chặn chạy song song, nó làm kết quả không an toàn/không xác định). Back mới: capturing an external mutable list makes the result unsafe because ArrayList cannot take concurrent writes. Front giữ nguyên nên CardKey không đổi.
- `jv-0005-5387bbeafb` "Which two arguments does Stream.max() ... require?" — **chờ quyết định**. Đáp án "Only a Comparator" là đúng; chính câu hỏi hỏi "two arguments" là sai. Sửa Front sẽ đổi CardKey (thẻ mới + xoá thẻ cũ), nên không tự làm.
