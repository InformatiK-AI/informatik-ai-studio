# gRPC Protocol Buffers Example: Blog API

Full example of a gRPC service definition using Protocol Buffers.

```protobuf
syntax = "proto3";

package blog.v1;

import "google/protobuf/timestamp.proto";
import "google/protobuf/empty.proto";

service BlogService {
  // List posts with pagination
  rpc ListPosts(ListPostsRequest) returns (ListPostsResponse);

  // Get a single post by ID
  rpc GetPost(GetPostRequest) returns (Post);

  // Create a new post
  rpc CreatePost(CreatePostRequest) returns (Post);

  // Update an existing post
  rpc UpdatePost(UpdatePostRequest) returns (Post);

  // Delete a post
  rpc DeletePost(DeletePostRequest) returns (google.protobuf.Empty);

  // Publish a post
  rpc PublishPost(PublishPostRequest) returns (Post);
}

message Post {
  string id = 1; // UUID
  string title = 2;
  string content = 3;
  bool published = 4;
  string author_id = 5; // UUID
  google.protobuf.Timestamp created_at = 6;
  google.protobuf.Timestamp updated_at = 7;
}

message ListPostsRequest {
  int32 page = 1;
  int32 page_size = 2; // Default: 20, Max: 100
  optional bool published = 3; // Filter by published status
}

message ListPostsResponse {
  repeated Post posts = 1;
  Pagination pagination = 2;
}

message Pagination {
  int32 page = 1;
  int32 page_size = 2;
  int32 total_count = 3;
  int32 total_pages = 4;
}

message GetPostRequest {
  string id = 1; // UUID
}

message CreatePostRequest {
  string title = 1;
  string content = 2;
  bool published = 3; // Default: false
}

message UpdatePostRequest {
  string id = 1; // UUID
  optional string title = 2;
  optional string content = 3;
  optional bool published = 4;
}

message DeletePostRequest {
  string id = 1; // UUID
}

message PublishPostRequest {
  string id = 1; // UUID
}

// Error handling
message Error {
  string code = 1;
  string message = 2;
  repeated FieldError details = 3;
}

message FieldError {
  string field = 1;
  string message = 2;
}
```
