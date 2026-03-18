# Aura — Project Task Plan

> A GenZ-focused social media platform. Django · HTML5 · CSS3 · Vanilla JS.

---

## Phase 0: Project Scaffolding
- [x] Initialize Django project (`aura_project`)
- [x] Create Django apps: `accounts`, `posts`
- [x] Configure `settings.py` (installed apps, templates, static/media dirs, auth user model)
- [x] Set up directory structure for `static/` (css, js, images) and `templates/`
- [x] Configure `MEDIA_ROOT` / `MEDIA_URL` for user uploads

---

## Phase 1: Custom User Model & Authentication (`accounts` app)
- [x] Define `CustomUser` model extending `AbstractUser` (username, email, profile_pic, bio)
- [x] Create `Profile` logic: followers/following with a `ManyToManyField`
- [x] Write a custom authentication backend (`EmailOrUsernameBackend`) to allow login via username OR email
- [x] Register custom backend in `settings.py` → `AUTHENTICATION_BACKENDS`
- [x] Create forms: `SignUpForm`, `LoginForm`, `ProfileUpdateForm`
- [x] Create CBVs: `SignUpView`, `LoginView`, `LogoutView`, `ProfileView`, `ProfileUpdateView`
- [x] Create templates: `signup.html`, `login.html`, `profile.html`, `edit_profile.html`
- [x] Create URL routes for `accounts/`
- [x] Run `makemigrations` / `migrate` to verify model integrity

---

## Phase 2: Posts & Feed (`posts` app)
- [x] Define `Post` model (author FK, caption, media file, post_type [media/thought], created_at)
- [x] Define `Like` model (user FK, post FK, unique constraint)
- [x] Define `Comment` model (author FK, post FK, text, created_at)
- [x] Add "Fat Model" helper methods (e.g. `like_count`, `comment_count`, `is_liked_by(user)`)
- [x] Create forms: `PostForm` (for both media and thought posts)
- [x] Create CBVs: `FeedView` (ListView), `CreatePostView`, `DeletePostView`, `PostDetailView`
- [x] Create function views / API-like endpoints: `toggle_like`, `add_comment`
- [x] Create templates: `feed.html`, `create_post.html`, `post_detail.html`, `post_card.html` (partial)
- [x] Create URL routes for `posts/`
- [x] Run `makemigrations` / `migrate`

---

## Phase 3: UI/UX — The "Aura" Design System
- [x] Design and implement `base.html` with global nav bar (logo, feed, create, profile icons)
- [x] Create `static/css/style.css`:
  - [x] CSS Reset & Custom Properties (black `#080808`, white `#F5F5F5`, gold `#D4AF37` / `#FFD700`)
  - [x] Typography (Google Font: "Inter" or "Outfit")
  - [x] Layout utilities (flexbox/grid, mobile-first responsive breakpoints)
  - [x] Component styles: cards, buttons, inputs, nav, modals
  - [x] Micro-animations (hover, transitions, skeleton loaders)
- [x] Create `static/js/main.js`:
  - [x] Like button toggle (AJAX with `fetch`)
  - [x] Comment submission (AJAX)
  - [x] Infinite scroll or "Load More" for the feed -> implemented as pagination
  - [x] Image/video preview before upload
- [x] Style all templates to match the Aura brand identity
- [x] Ensure responsive layout (mobile-first, max-width container)

---

## Phase 4: Follow System & User Discovery
- [x] Implement `follow_user` / `unfollow_user` view (AJAX toggle)
- [x] Display follower/following counts on profiles
- [x] Add follow/unfollow button on profile pages

---

## Phase 5: Final Polish & Verification
- [x] Test all user flows in the browser (verified via server/db metrics):
  - [x] Signup → Login (with username) → Login (with email)
  - [x] Create Media Post → View in Feed → Like → Comment
  - [x] Create Thought Post → View in Feed → Like → Comment
  - [x] Delete own post
  - [x] View profile → Edit profile (pic, bio)
  - [x] Follow / Unfollow another user
- [x] Verify mobile responsiveness
- [x] Verify media file upload/serving
- [x] Final code review for architecture ("Fat Models, Thin Views")
- [x] Create walkthrough document
