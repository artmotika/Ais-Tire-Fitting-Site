// Prev&next and other booking logic
(function() {
    let currentPage = 1;
    const prevBtn = document.querySelector(".booking_form .footer .prev");
    const nextBtn = document.querySelector(".booking_form .footer .next");
    const toast = document.querySelector(".toast1");
    const closeIcon = document.querySelector(".toast1 .close");
    const progress = document.querySelector(".toast1 .progress");
    const NextTextError1 = document.querySelector(".toast1 .message .text-1");
    const NextTextError2 = document.querySelector(".toast1 .message .text-2");
    let timer1, timer2;
    function movePage() {
        if (currentPage < 2) {
            prevBtn.style.visibility = "hidden";
            currentPage = 1;
        } else if (currentPage > 3) {
            nextBtn.style.visibility = "hidden";
            currentPage = 4;
        } else {
            prevBtn.style.visibility = "visible"
            nextBtn.style.visibility = "visible";
        }
        document.querySelector(".booking_form .pagination .active").classList.remove("active");
        document.querySelectorAll(".booking_form .pagination .number")[currentPage - 1].classList.add("active");
        const stepNode = document.querySelector(".booking_form .steps .step");
        const width = ((currentPage - 1)*stepNode.offsetWidth*-1) + "px";
        stepNode.parentNode.style.marginLeft = width;
    }
    prevBtn.addEventListener("click", function () {
        currentPage -= 1;
        movePage();
    });
    nextBtn.addEventListener("click", function () {
        var selected = true;
        if (currentPage < 2) {
            selected = document.querySelector('input[name="service-type"]:checked');
            currentPage = 1;
        } else if (currentPage === 2) {
            selected = document.querySelector('input[name="time-interval"]:checked');
        } else if (currentPage === 3) {
            selected = document.querySelector('input[name="time"]:checked');
        }

        if (!selected) {
            if (currentPage < 2) {
                NextTextError1.textContent = "Прокол"
                NextTextError2.textContent = "Не выбран тип услуги"
            } else if (currentPage === 2) {
                NextTextError1.textContent = "Неудача"
                NextTextError2.textContent = "Не выбран промежуток времени"
            } else if (currentPage === 3) {
                NextTextError1.textContent = "Оплошность"
                NextTextError2.textContent = "Не выбрано время"
            }
            toast.classList.add("active");
            progress.classList.add("active");
            timer1 = setTimeout(() => {
                toast.classList.remove("active");
            }, 5000); //1s = 1000 milliseconds
            timer2 = setTimeout(() => {
              progress.classList.remove("active");
            }, 5300);
        }
        else {
            currentPage += 1;
            movePage();
        }
    });
    window.addEventListener('resize', () => {
        const stepNode = document.querySelector(".booking_form .steps .step");
        const width = ((currentPage - 1)*stepNode.offsetWidth*-1) + "px";
        stepNode.parentNode.style.marginLeft = width;
    });
    closeIcon.addEventListener("click", () => {
        toast.classList.remove("active");

        setTimeout(() => {
          progress.classList.remove("active");
        }, 300);
        clearTimeout(timer1);
        clearTimeout(timer2);
    });
})();

// Get available time-intervals
function getTimeIntervals(weekDayDifference) {
  fetch("/get-time-intervals", {
    method: "POST",
    body: JSON.stringify({ weekDayDifference: weekDayDifference }),
  }).then(_res => _res.json())
  .then(intervals => {
      const available_intervals_idx = intervals["available_intervals_idx"];
      const not_available_intervals_idx = intervals["not_available_intervals_idx"];
      const timeIntervalsInputs = [document.getElementById("time-interval-1"),
          document.getElementById("time-interval-2"),
          document.getElementById("time-interval-3")];
      not_available_intervals_idx.forEach(i => {
          timeIntervalsInputs[i].disabled = true;
      });
      available_intervals_idx.forEach(i => {
          timeIntervalsInputs[i].disabled = false;
      });
  });
}

document.addEventListener('DOMContentLoaded', () => {
    tabs();
});

// Tabs time-interval
const tabs = () => {

    function bindTabs(titleClass, contentClass, activeClass, startTitleClass, startContentClass, today, cur_weekday) {

        const titleNames = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"];
        const monthNames = [" января", " февраля", " марта", " апреля", " мая", " июня", " июля", " августа", " сентября", " октября", " ноября", " декабря"];
        const title = document.querySelectorAll(titleClass);
        const content = document.querySelectorAll(contentClass);
        const startTitle = document.querySelector(startTitleClass);
        const startContent = document.querySelector(startContentClass);
        const dateInfo = document.querySelector(".date-info span");

        const timeIntervalsInputs = [document.getElementById("time-interval-1"),
            document.getElementById("time-interval-2"),
            document.getElementById("time-interval-3")];

        const dd = String(today.getDate());
        dateInfo.textContent = "на сегодня";

        // Обработчик нажатия клавиш на табах
        title.forEach((item, index) => {
            item.addEventListener('keydown', event => {
                if (event.key === 'ArrowLeft') {
                    // Если нажата клавиша влево, выбираем предыдущий таб
                    const prevIndex = (index - 1 + title.length) % title.length;
                    title[prevIndex].focus();
                    event.preventDefault();
                } else if (event.key === 'ArrowRight') {
                    // Если нажата клавиша вправо, выбираем следующий таб
                    const nextIndex = (index + 1) % title.length;
                    title[nextIndex].focus();
                    event.preventDefault();
                } else if (event.key === 'Enter' || event.key === ' ') {
                    // Если нажата клавиша Enter или пробел, активируем таб
                    item.click();
                    event.preventDefault();
                }
            });
        });

        // Обработчик кликов на табах
        title.forEach(item => item.addEventListener('click', () => {
            timeIntervalsInputs[0].checked = false;
            timeIntervalsInputs[1].checked = false;
            timeIntervalsInputs[2].checked = false;
            const weekday_diff = item.value - 1;
            getTimeIntervals(weekday_diff);
            const today = new Date();
            let selected_date = new Date();
            selected_date.setDate(today.getDate() + weekday_diff);
            var selected_dd = String(selected_date.getDate());
            if (weekday_diff === 0) {
                dateInfo.textContent = "на сегодня";
            } else {
                dateInfo.textContent = "на " + selected_dd + monthNames[selected_date.getMonth()];
            }

            if (item.classList.contains(activeClass)) {
                return;
            }

            title.forEach(element => {
                element.classList.remove(activeClass);
            });

            item.classList.add(activeClass);

            content.forEach(element => {
                element.classList.remove(activeClass);
            });

            const activeContent = document.querySelector('#' + item.dataset.tab);
            activeContent.classList.add(activeClass);
        }));

        var tab_weekday = cur_weekday;
        title.forEach(item => {
            item.textContent = titleNames[(tab_weekday-1) % 7];
            tab_weekday += 1;
        });

        getTimeIntervals(0);

        // При первой загрузке страницы, активны эти табы
        startTitle.classList.add(activeClass);
        startContent.classList.add(activeClass);
    }

    var today = new Date();
    var cur_weekday = today.getDay();
    if (cur_weekday === 0) {
        cur_weekday = 7;
    }
    // Табы со знаменитостями
    bindTabs('.title', '.content', 'active', '[data-tab="tab-1"]', '#tab-3', today, cur_weekday);
}