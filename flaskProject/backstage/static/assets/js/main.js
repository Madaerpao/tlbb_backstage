;
(function ($) {
    "use strict";
    jQuery(document).ready(function () {

        $('.menu-icon').on('click', function (e) {
            e.preventDefault();
            $('.offcanvas').addClass('show').removeClass('hide');
        });

        $('.close').on('click', function (e) {
            e.preventDefault();
            $('.offcanvas').addClass('hide').removeClass('show');
        });

        // == Hero Slider== //

        var swiper = new Swiper('.hero-slider', {
            autoplay: {
                delay: 2500,
                disableOnInteraction: true,
            },
            speed: 900,
            loop: true,
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
                renderBullet: function (index, className) {
                    return '<span class="' + className + '">' + (index + 1) + '</span>';
                },
            },
            navigation: {
                nextEl: '.arr-right',
                prevEl: '.arr-left',
            },
            on: {
                slideChangeTransitionStart: function () {
                    $('.slider-content h4, .slider-content h5, .hero-btn, .slide-img img').removeClass('aos-init').removeClass('aos-animate');
                },
                slideChangeTransitionEnd: function () {
                    AOS.init();
                },
            },
        });
        $(".hero-slider").hover(function () {
            (this).swiper.autoplay.stop();
        }, function () {
            (this).swiper.autoplay.start();
        });

        AOS.init({
            disable: 'mobile'
        });

        // == Book Tab == //

        var filterizd = $('.filtr-container').filterizr({
            //options object
        });

        $('.filter-tabs li').on('click', function (e) {
            e.preventDefault();
            $('.filter-tabs li.active').removeClass('active');
            $(this).addClass('active');
        });

        // == Review Slider == //

        var swiper2 = new Swiper('.review-slider', {
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
        });

        var swiper3 = new Swiper('.post-slider', {
            pagination: {
                el: '.swiper-paginations',
                clickable: true,
            },
        });

        // == Instafeed Slider == //

        var swiper4 = new Swiper('.instafeed-slider', {
            slidesPerView: 6,
            spaceBetween: 0,
            autoplay: {
                delay: 2500,
                disableOnInteraction: false,
            },
            breakpoints: {
                1024: {
                    slidesPerView: 4,
                },
                768: {
                    slidesPerView: 3,
                },
                640: {
                    slidesPerView: 2,
                },
                320: {
                    slidesPerView: 1,
                }
            }
        });

        // == Social Link Slider == //

        var swiper5 = new Swiper('.social-slider', {
            simulateTouch: true,
            slidesPerView: 7,
            breakpoints: {
                1200: {
                    slidesPerView: 6,
                },
                1024: {
                    slidesPerView: 5,
                },
                768: {
                    slidesPerView: 4,
                },
                640: {
                    slidesPerView: 3,
                },
                320: {
                    slidesPerView: 2,
                }
            }
        });

        // == Back To Top Button == //

        if ($('#back-to-top').length) {
            $('#back-to-top').on('click', function (e) {
                e.preventDefault();
                $('html,body').animate({
                    scrollTop: 0
                }, 700);
            });
        }
    });

    jQuery(window).on('load', function () {

        // == Animated Page Loader == //

        if ($.fn.loaders) {
            $('.loader-inner').loaders();
        }

        // == Animate loader off screen == //

        $(".css-loader").fadeOut("slow");

    });
})(jQuery)