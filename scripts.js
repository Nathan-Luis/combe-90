// scripts.js
$(document).ready(function() {
  $("#hero-carousel").owlCarousel({
    items: 1,
    loop: true,
    nav: true,
    dots: true,
    autoplay: true,
    autoplayTimeout: 5000,
    animateOut: 'fadeOut',
    animateIn: 'fadeIn',
  });

  $("#services-carousel").owlCarousel({
    items: 3,
    margin: 10,
    loop: true,
    nav: true,
    dots: true,
    autoplay: true,
    autoplayTimeout: 5000,
    responsive: {
      0: {
        items: 1
      },
      600: {
        items: 2
      },
      1000: {
        items: 3
      }
    }
  });

  $("#clients-carousel").owlCarousel({
    items: 4,
    margin: 10,
    loop: true,
    nav: true,
    dots: true,
    autoplay: true,
    autoplayTimeout: 5000,
    responsive: {
      0: {
        items: 1
      },
      600: {
        items: 2
      },
      1000: {
        items: 4
      }
    }
  });

  // Parallax effect
  $('[data-parallax-img]').each(function() {
    var $el = $(this);
    var imgSrc = $el.data('parallax-img');

    $el.css({
      'background-image': 'url(' + imgSrc + ')',
      'background-attachment': 'fixed',
      'background-size': 'cover',
      'background-position': 'center'
    });

    $(window).scroll(function() {
      var scrollTop = $(window).scrollTop();
      var offset = $el.offset().top;
      var height = $el.outerHeight();
      var windowHeight = $(window).height();

      if (offset + height <= scrollTop || offset >= scrollTop + windowHeight) {
        return;
      }

      var yBgPosition = Math.round((offset - scrollTop) * 0.5);
      $el.css('background-position', 'center ' + yBgPosition + 'px');
    });
  });
});

$(document).ready(function () {
  $('.counter').each(function () {
      var $this = $(this),
          countTo = $this.attr('data-count');
          
      $({ countNum: $this.text() }).animate({
          countNum: countTo
      },
      {
          duration: 2000,
          easing: 'swing',
          step: function () {
              $this.text(Math.floor(this.countNum));
          },
          complete: function () {
              $this.text(this.countNum);
          }
      });
  });
});


$(document).ready(function(){
  $("#about-us-carousel").owlCarousel({
    items: 3, // Show 2 items at a time
    loop: true,
    margin: 10,
    nav: true,
    dots: false,
    autoplay: true,
    autoplayTimeout: 5000,
    autoHeight: true
  });
});

// Fix for cart functionality
let cart = JSON.parse(localStorage.getItem('cart')) || [];

function addToCart(button) {
  const product = button.closest('.product');
  const name = product.getAttribute('data-name');
  const price = parseFloat(product.getAttribute('data-price'));
  const quantity = parseInt(product.querySelector('.quantity-input').value);

  if (quantity <= 0) {
    alert('You cannot add zero items to the cart');
    return;
  }

  const existingItem = cart.find(item => item.name === name);
  if (existingItem) {
    existingItem.quantity += quantity;
  } else {
    cart.push({ name, price, quantity });
  }

  localStorage.setItem('cart', JSON.stringify(cart));
  updateCartDisplay();
  alert('Added to cart');
}

function updateCartDisplay() {
  const cartItemsElement = document.getElementById('cart-items');
  cartItemsElement.innerHTML = '';
  cart.forEach(item => {
    const li = document.createElement('li');
    li.textContent = `${item.name} - R${item.price} x ${item.quantity}`;
    cartItemsElement.appendChild(li);
  });
}

function showDetails(button) {
  const product = button.closest('.product');
  const name = product.getAttribute('data-name');
  const description = product.getAttribute('data-description');
  const imgSrc = product.querySelector('img').src;

  document.getElementById('details-image').src = imgSrc;
  document.getElementById('details-description').textContent = description;
  document.getElementById('details-modal').style.display = 'block';
}

function closeModal() {
  document.getElementById('details-modal').style.display = 'none';
}

window.onload = updateCartDisplay;

$(document).ready(function() {
  // Owl Carousel Initialization
  $('.owl-carousel').owlCarousel({
      loop: true,
      margin: 10,
      nav: true,
      responsive: {
          0: {
              items: 1
          },
          600: {
              items: 3
          },
          1000: {
              items: 5
          }
      }
  });

  // Modal handling
  function closeModal() {
      $('#details-modal').hide();
  }

  window.closeModal = closeModal;

  function showDetails(button) {
      const product = $(button).closest('.product');
      const name = product.data('name');
      const description = product.data('description');
      const imgSrc = product.find('img').attr('src');

      $('#details-image').attr('src', imgSrc);
      $('#details-description').text(description);
      $('#details-modal').show();
  }

  window.showDetails = showDetails;

  // Update Cart Display
  function updateCartDisplay() {
      const cart = JSON.parse(localStorage.getItem('cart')) || [];
      const cartItemsElement = $('#cart-items');
      cartItemsElement.empty();
      cart.forEach(item => {
          const li = $('<li>').text(`${item.name} - R${item.price} x ${item.quantity}`);
          cartItemsElement.append(li);
      });
  }

  function addToCart(button) {
      const product = $(button).closest('.product');
      const name = product.data('name');
      const price = parseFloat(product.data('price'));
      const quantity = parseInt(product.find('.quantity-input').val());

      if (quantity <= 0) {
          showNotification('You cannot add zero items to the cart', button);
          return;
      }

      let cart = JSON.parse(localStorage.getItem('cart')) || [];
      const existingItem = cart.find(item => item.name === name);
      if (existingItem) {
          existingItem.quantity += quantity;
      } else {
          cart.push({ name, price, quantity });
      }

      localStorage.setItem('cart', JSON.stringify(cart));
      updateCartDisplay();
      showNotification('Added to cart', button);
  }

  window.addToCart = addToCart;

  // Show Notification
  function showNotification(message, button) {
      const notification = $('#notification');
      notification.text(message);
      notification.css({
          display: 'block',
          top: `${$(button).offset().top - 30}px`,
          left: `${$(button).offset().left}px`
      });

      setTimeout(() => {
          notification.fadeOut();
      }, 3000);
  }

  // Filtering products
  function filterProducts() {
      const searchQuery = $('#search-input').val().toLowerCase();
      const selectedCategory = $('#category-filter').val();
      const selectedPriceRange = $('#price-filter').val();

      $('.product').each(function() {
          const name = $(this).data('name').toLowerCase();
          const category = $(this).data('category').split(' ');
          const price = parseFloat($(this).data('price'));

          let isVisible = true;

          if (searchQuery && !name.includes(searchQuery)) {
              isVisible = false;
          }

          if (selectedCategory && !category.includes(selectedCategory)) {
              isVisible = false;
          }

          if (selectedPriceRange) {
              const [minPrice, maxPrice] = selectedPriceRange.split('-').map(parseFloat);
              if (price < minPrice || price > maxPrice) {
                  isVisible = false;
              }
          }

          if (isVisible) {
              $(this).show();
          } else {
              $(this).hide();
          }
      });
  }

  $('#search-input').on('input', filterProducts);
  $('#category-filter').on('change', filterProducts);
  $('#price-filter').on('change', filterProducts);

  // Initialize cart display on page load
  updateCartDisplay();
});

function updateCartDisplay() {
  const cartItemsElement = document.getElementById('cart-items');
  if (cartItemsElement) {
      cartItemsElement.innerHTML = '';
      cart.forEach(item => {
          const li = document.createElement('li');
          li.textContent = `${item.name} - R${item.price} x ${item.quantity}`;
          cartItemsElement.appendChild(li);
      });
  }
}

$(document).ready(function() {
  // Show service details modal
  function showServiceDetails(service) {
      const serviceTitle = $(service).find('h4').text();
      const serviceDescription = $(service).find('p').text();
      const serviceImage = $(service).find('img').attr('src');

      $('#service-title').text(serviceTitle);
      $('#service-description').text(serviceDescription);
      $('#service-image').attr('src', serviceImage);

      $('#survey-type').val(serviceTitle); // Pre-fill survey type with the service name

      $('#service-details-modal').show();
  }

  // Close modal
  $('.close').click(function() {
      $('#service-details-modal').hide();
  });

  // Show service details on 'Read More' click
  $('.button-primary').click(function(event) {
      event.preventDefault();
      showServiceDetails($(this).closest('.service-box'));
  });

  // Handle survey form submission
  $('#survey-form').submit(function(event) {
      event.preventDefault();

      // Submit the form to the server
      this.submit();

      // Show success message and hide modal
      alert("Survey requested successfully!");
      $('#service-details-modal').hide();
  });
});


// scripts.js

// Toggle navigation menu on clicking hamburger icon
function toggleMenu() {
  var navMenu = document.getElementById("nav-menu");
  navMenu.classList.toggle("active");
}

// Ensure the event listener is added after the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
  const hamburger = document.querySelector('.hamburger');
  const navMenu = document.getElementById("nav-menu");

  if (hamburger) {
      console.log("Hamburger icon found, adding click event listener.");
      hamburger.addEventListener('click', function() {
          navMenu.classList.toggle("active");
          console.log("Hamburger clicked, menu class toggled.");
      });
  } else {
      console.log("Hamburger icon not found.");
  }
});


