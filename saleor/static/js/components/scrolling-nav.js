(function($) {
  "use strict"; // Start of use strict

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 50)
        }, 1000, "easeInOutExpo");
        return false;
      }
  }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function() {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 56
  });

  // Hide Header on on scroll down
  var didScroll;
  var lastScrollTop = 0;
  var delta = 5;
  var navbarHeight = $('nav').outerHeight();

  // Scrolling Effect
  $(window).on("scroll", function() {
    didScroll = true;
  });

  setInterval(function() {
    if (didScroll) {
      hasScrolled();
      didScroll = false;
    }
  }, 250);

  function hasScrolled() {
    var st = $(window).scrollTop();
    console.log("st = " + st);
    console.log("lastScrollTop = " + lastScrollTop);
    console.log("navbarHeight = " + navbarHeight);    // Make sure they scroll more than delta
    if (Math.abs(lastScrollTop - st) <= delta)
      return;

    // If they scrolled down and are past the navbar, add class .nav-up.
    // This is necessary so you never see what is "behind" the navbar.

    if (st > lastScrollTop && st > navbarHeight) {
      // Scroll Down
      $('nav').addClass('nav-up');
      console.log('scrolled down')
    } else {
      // Scroll Up
      console.log('scrolled up');
      if (st + $(window).height() < $(document).height()) {
        $('nav').removeClass('nav-up');
      }
    }
    lastScrollTop = st;
  }



})(jQuery); // End of use strict
