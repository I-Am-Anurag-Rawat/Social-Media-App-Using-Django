//Ajax for like functionality and like count
document.querySelectorAll('.like-form').forEach(form => {
  form.addEventListener('submit', function(e) {
    e.preventDefault();

    const url = this.action;
    const csrfToken = this.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken,
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    .then(res => res.json())
    .then(data => {
      const postContainer = this.closest('.post-container');
      const likeCount = postContainer.querySelector('.like-count');
      const button = this.querySelector('.like-button');
      //const likeCount = this.querySelector('.like-count');
      likeCount.textContent = `❤️ ${data.like_count} Like${data.like_count !== 1 ? 's' : ''}`;
      if (data.liked) {
        button.textContent = '❤️ Liked';
        button.classList.add('text-red-500');
        button.classList.remove('text-gray-600');
        //likeCount.textContent = "❤️ " + data.like_count + " Like" + (data.like_count === 1 ? "" : "s");
      } else {
        button.textContent = '🤍 Like';
        button.classList.add('text-gray-600');
        button.classList.remove('text-red-500');
        //likeCount.textContent = "❤️ " + data.like_count + " Like" + (data.like_count === 1 ? "" : "s");
      }
    })
    .catch(err => console.error('AJAX error:', err));
  });
})
// Helper to get CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let cookie of cookies) {
          cookie = cookie.trim();
          if (cookie.startsWith(name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
<script src="{% static 'core/home.js' %}"></script>

//Ajax for comment functionality and comment count