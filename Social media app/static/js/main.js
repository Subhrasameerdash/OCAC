/* ═══════════════════════════════════════════════════════════════════════
   AURA — Main JavaScript
   Handles: Likes, Comments (AJAX), Media Preview, Follow, Nav Toggle
   ═══════════════════════════════════════════════════════════════════════ */

(function () {
    'use strict';

    // ── Helpers ──────────────────────────────────────────────────────
    function getCookie(name) {
        const cookies = document.cookie.split(';');
        for (let c of cookies) {
            c = c.trim();
            if (c.startsWith(name + '=')) {
                return decodeURIComponent(c.substring(name.length + 1));
            }
        }
        return null;
    }

    const csrfToken = getCookie('csrftoken');

    function postJSON(url, body = {}) {
        return fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(body),
        }).then(res => res.json());
    }

    // ── Mobile Nav Toggle ───────────────────────────────────────────
    const navToggle = document.getElementById('nav-mobile-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('open');
        });
    }

    // ── Like Toggle ─────────────────────────────────────────────────
    document.addEventListener('click', function (e) {
        const btn = e.target.closest('.like-btn');
        if (!btn) return;

        e.preventDefault();
        const postId = btn.dataset.postId;

        postJSON(`/${postId}/like/`).then(data => {
            const countEl = document.getElementById(`like-count-${postId}`);

            if (data.liked) {
                btn.classList.add('liked', 'pop');
            } else {
                btn.classList.remove('liked');
                btn.classList.add('pop');
            }

            if (countEl) {
                countEl.textContent = `${data.like_count} likes`;
            }

            // Remove pop animation class after it completes
            setTimeout(() => btn.classList.remove('pop'), 400);
        }).catch(err => console.error('Like error:', err));
    });

    // ── Comment Submit ──────────────────────────────────────────────
    const commentForm = document.getElementById('comment-form');

    if (commentForm) {
        commentForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const postId = this.dataset.postId;
            const input = document.getElementById('comment-input');
            const text = input.value.trim();
            if (!text) return;

            postJSON(`/${postId}/comment/`, { text }).then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }

                // Remove "no comments" message
                const noComments = document.getElementById('no-comments');
                if (noComments) noComments.remove();

                // Append new comment
                const list = document.getElementById('comments-list');
                const commentHTML = `
                    <div class="comment" id="comment-${data.id}">
                        <a href="/accounts/profile/${data.author}/" class="comment-author-link">
                            <img src="${data.author_pic}" alt="${data.author}" class="comment-avatar">
                        </a>
                        <div class="comment-body">
                            <a href="/accounts/profile/${data.author}/" class="comment-author-name">${data.author}</a>
                            <p class="comment-text">${escapeHTML(data.text)}</p>
                            <span class="comment-time">Just now</span>
                        </div>
                    </div>
                `;
                list.insertAdjacentHTML('beforeend', commentHTML);

                // Update comment count on the post card
                const countLink = document.querySelector('.comment-count-link');
                if (countLink) {
                    countLink.textContent = `${data.comment_count} comments`;
                }

                // Scroll to new comment
                list.scrollTop = list.scrollHeight;
                input.value = '';
            }).catch(err => console.error('Comment error:', err));
        });
    }

    function escapeHTML(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    // ── Media Preview (Create Post) ─────────────────────────────────
    const fileInput = document.getElementById('id_media');
    const previewContainer = document.getElementById('media-preview');
    const previewImg = document.getElementById('preview-img');
    const previewVideo = document.getElementById('preview-video');
    const removeBtn = document.getElementById('remove-preview');
    const uploadLabel = document.querySelector('.upload-label');

    if (fileInput && previewContainer) {
        fileInput.addEventListener('change', function () {
            const file = this.files[0];
            if (!file) return;

            const url = URL.createObjectURL(file);

            if (file.type.startsWith('video/')) {
                previewVideo.src = url;
                previewVideo.style.display = 'block';
                previewImg.style.display = 'none';
            } else {
                previewImg.src = url;
                previewImg.style.display = 'block';
                previewVideo.style.display = 'none';
            }

            previewContainer.style.display = 'block';
            if (uploadLabel) uploadLabel.style.display = 'none';
        });

        if (removeBtn) {
            removeBtn.addEventListener('click', function () {
                fileInput.value = '';
                previewContainer.style.display = 'none';
                previewImg.style.display = 'none';
                previewVideo.style.display = 'none';
                if (uploadLabel) uploadLabel.style.display = 'flex';
            });
        }
    }

    // ── Avatar Preview (Edit Profile) ───────────────────────────────
    const avatarInput = document.getElementById('id_profile_pic');
    const avatarPreview = document.getElementById('avatar-preview');

    if (avatarInput && avatarPreview) {
        avatarInput.addEventListener('change', function () {
            const file = this.files[0];
            if (file) {
                avatarPreview.src = URL.createObjectURL(file);
            }
        });
    }

    // ── Follow / Unfollow ───────────────────────────────────────────
    document.addEventListener('click', function (e) {
        const btn = e.target.closest('.follow-btn');
        if (!btn) return;

        e.preventDefault();
        const userId = btn.dataset.userId;

        postJSON(`/accounts/follow/${userId}/`).then(data => {
            if (data.following) {
                btn.textContent = 'Following';
                btn.classList.remove('btn-gold');
                btn.classList.add('btn-outline');
            } else {
                btn.textContent = 'Follow';
                btn.classList.remove('btn-outline');
                btn.classList.add('btn-gold');
            }

            const followersCount = document.getElementById('followers-count');
            if (followersCount) {
                followersCount.textContent = data.follower_count;
            }
        }).catch(err => console.error('Follow error:', err));
    });

    // ── Auto-dismiss flash messages ─────────────────────────────────
    const messages = document.querySelectorAll('.message');
    messages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-12px)';
            setTimeout(() => msg.remove(), 300);
        }, 4000);
    });

})();
