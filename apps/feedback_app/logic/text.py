from typing import Dict

no_visited_clinics_text = {
    'uz': "❗ Fikr bildirish uchun tashrif buyurgan klinikangiz yo‘q.",
    'ru': "❗ У вас нет посещённых клиник для оставления отзыва."
}

choice_feedback_text = {
    'uz': 'Quyidagi variantlardan birini tanlang:',
    'ru': 'Пожалуйста, выберите один из вариантов ниже:'
}

# error
backend_error_text: Dict[str, str] = {
    'uz': "❗ Maʼlumotlarni olishda xatolik yuz berdi. Iltimos, keyinroq urinib ko‘ring.",
    'ru': "❗ Ошибка при получении данных. Пожалуйста, попробуйте позже."
}

write_comment_text: Dict[str, str] = {
    'uz': "Iltimos, fikringizni biz bilan bo‘lishing. Sizning fikringiz biz uchun muhim!",
    'ru': "Пожалуйста, поделитесь своим мнением. Ваш отзыв важен для нас!"
}

feedback_text = {
    'uz': "Fikr bildirish uchun klinikani tanlang",
    'ru': "Выберите клинику для отзыва"
}

feedback_post_button = {
    'uz': "📝 Fikr qoldirish",  # Оставить отзыв
    'ru': "📝 Оставить отзыв"
}

feedback_list_button = {
    'uz': "📋 Klinikaga fikrlar",  # Отзывы о клинике
    'ru': "📋 Отзывы о клинике"
}

# Translateable labels
feedback_labels = {
    "uz": {
        "title": "📍 *Klinikaga bildirilgan fikrlar:* _{clinic}_",
        "score": "⭐ Baho",
        "comment": "💬 Izoh",
        "no_comment": "Izoh yo‘q",
        "date": "📅 Sana"
    },
    "ru": {
        "title": "📍 *Отзывы по клинике:* _{clinic}_",
        "score": "⭐ Оценка",
        "comment": "💬 Комментарий",
        "no_comment": "Нет комментария",
        "date": "📅 Дата"
    }
}

score_text = {
    'uz': (
        "Klinika: {clinic_name} - {branch}\n"
        "Tashrif sanasi: {visit_date}\n\n"
        "Tajribangizni 1 dan 5 gacha yulduzcha bilan baholang ⭐️:"
    ),
    'ru': (
        "Клиника: {clinic_name} - {branch}\n"
        "Дата визита: {visit_date}\n\n"
        "Оцените ваш визит от 1 до 5 звёзд ⭐️:"
    )
}

data_not_found_text = {
    'uz': "Maʼlumot topilmadi. Iltimos, yana urinib ko‘ring.",
    'ru': "Данные не найдены. Пожалуйста, попробуйте снова.",
}

score_less_3_text = {
    'uz': "Iltimos, baho berish sababini yozing. Bu bizga xizmatlarimizni yaxshilashda yordam beradi.",
    'ru': "Пожалуйста, укажите причину такой оценки. Это поможет нам стать лучше.",
}

feedback_thanks_text = {
    'uz': "Bahoyingiz uchun rahmat! 🌟",
    'ru': "Спасибо за вашу оценку! 🌟",
}
invalid_data_clinic = {
    'uz': "❌ Klinikaga oid ma'lumotlar noto‘g‘ri.",
    'ru': "❌ Неверные данные клиники."
}

no_feedback_text = {
    'uz': "😔 Hozircha fikrlar yo‘q.",
    'ru': "😔 Отзывов пока нет."
}
