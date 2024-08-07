$(document).ready(function () {
  const sliderPrevArrowTemplate = `<button class="slider-arrow prev w-[32px] h-[32px] ">
            <svg xmlns="http://www.w3.org/2000/svg"  fill="currentColor" class="w-[24px] h-[24px]  md:w-[28px] md:h-[28px] text-brand-primary" viewBox="0 0 16 16">
                <path d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0zm3.5 7.5a.5.5 0 0 1 0 1H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5H11.5z"/>
            </svg>
        </button>`
  const sliderNextArrowTemplate = `<button type="button" class="slider-arrow next w-[32px] h-[32px] text-brand-primary">
                                <svg xmlns="http://www.w3.org/2000/svg"  fill="currentColor" class="w-[24px] h-[24px]  md:w-[28px] md:h-[28px] text-brand-primary" viewBox="0 0 16 16">
                                  <path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0zM4.5 7.5a.5.5 0 0 0 0 1h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5H4.5z"/>
                                </svg>
                                </button>`


  $('.slider-3').slick({
    infinite: true,
    slidesToShow: 3,
    slidesToScroll: 1,
    prevArrow: sliderPrevArrowTemplate,
    nextArrow: sliderNextArrowTemplate,
    dots: false,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 2,
        }
      },
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 1,
        }
      }

    ]
  });

  $('.slider-4').slick({
    infinite: true,
    slidesToShow: 4,
    slidesToScroll: 1,
    prevArrow: sliderPrevArrowTemplate,
    nextArrow: sliderNextArrowTemplate,
    dots: false,

    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 3,
        }
      },
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 2,
        }
      }

    ]
  });

  $('.slider-6').slick({
    infinite: true,
    slidesToShow: 6,
    slidesToScroll: 1,
    prevArrow: sliderPrevArrowTemplate,
    nextArrow: sliderNextArrowTemplate,
    dots: false,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 4,
        }
      },
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 2,
        }
      }

    ]
  });

  function hideSpinner() {
    const spinner = $('.loadingSpinner');
    if (spinner.length) {
      setTimeout(function () {
        spinner.hide();
      }, 300);
    }
  }

  hideSpinner();


})