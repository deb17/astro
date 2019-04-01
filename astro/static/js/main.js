$('#responsiveTabsMain').responsiveTabs({
    startCollapsed: 'accordion'
});
$(document).ready(function(){
  $('.my-carousel').slick({
    dots: true,
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 4000,
    responsive: [
      {
        breakpoint: 600,
        settings: {
          mobileFirst: true
        }
      }
    ]
  });
});
$('#li-one, .r-tabs-accordion-title:first').click(function () {
  $('.my-carousel').slick("slickGoTo", 0, true);
});
