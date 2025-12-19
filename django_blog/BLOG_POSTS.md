# Blog Post Management Features

## List Posts
Accessible to all users at `/posts/`.

## View Post
Accessible to all users at `/posts/<id>/`.

## Create Post
Only authenticated users can create posts.
Author is set automatically.

## Edit & Delete Post
Only the post author can edit or delete their post.

## Security
- LoginRequiredMixin restricts access
- UserPassesTestMixin enforces ownership
- CSRF protection enabled
