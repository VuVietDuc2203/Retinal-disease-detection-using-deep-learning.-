Crop.py
Mô tả:
Tệp mã này thực hiện cắt ảnh bằng cách sử dụng OpenCV. 

Sử dụng
Để sử dụng mã này, làm theo các bước sau:
Thực thi các ô trong cuốn sổ để thực hiện cắt ảnh.


Blur12.py
Mô tả:
Tệp mã này áp dụng hiệu ứng mờ vào ảnh bằng cách sử dụng OpenCV. Nó được thiết kế để chạy trong một môi trường Colaboratory.
Sử dụng
Để sử dụng mã này, làm theo các bước sau:
Thực thi các ô trong cuốn sổ để áp dụng hiệu ứng mờ vào ảnh.


VGG16.py
Mô tả:
Tệp mã này huấn luyện một mô hình mạng nơ-ron dựa trên VGG16 để phân loại ảnh bằng cách sử dụng Keras và TensorFlow. Nó sử dụng kiến trúc VGG16 và tập dữ liệu RFMiD. Mô hình được huấn luyện trên một tập hình ảnh huấn luyện và được đánh giá trên một tập hình ảnh xác thực.

Sử dụng
Để sử dụng mã này, làm theo các bước sau:
Đảm bảo rằng bạn đã cài đặt các phụ thuộc cần thiết (Keras, TensorFlow, OpenCV, v.v.).
Đặt các đường dẫn phù hợp cho thư mục hình ảnh huấn luyện và xác thực trong mã.
Thực thi mã để huấn luyện mô hình VGG16 và đánh giá hiệu suất của nó.


Test.py
Mô tả:
Tệp mã này đánh giá một mô hình VGG16 đã được huấn luyện trước trên một tập dữ liệu kiểm tra và tạo ra các độ đo phân loại và ma trận nhầm lẫn. Nó sử dụng tập dữ liệu RFMiDgoc và tệp mô hình trước được đặt tên là "VGG164.h5".

Sử dụng
Để sử dụng mã này, làm theo các bước sau:
Đảm bảo rằng bạn đã cài đặt các phụ thuộc cần thiết (Keras, TensorFlow, OpenCV, v.v.).
Đặt các đường dẫn phù hợp cho thư mục hình ảnh kiểm tra và tệp mô hình đã được huấn luyện trước trong mã.
Thực thi mã để đánh giá mô hình và tạo ra các độ đo phân loại và ma trận nhầm lẫn.
