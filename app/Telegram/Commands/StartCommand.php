<?php

namespace App\Telegram\Commands;

use App\Models\User;
use SergiX44\Nutgram\Nutgram;
use SergiX44\Nutgram\Telegram\Types\Keyboard\KeyboardButton;
use SergiX44\Nutgram\Telegram\Types\Keyboard\ReplyKeyboardMarkup;

class StartCommand
{
    public function __invoke(Nutgram $bot): void
    {
        $telegram_user_id = $bot->message()->from->id;
        $username = $bot->message()->from->username;
        $first_name = $bot->message()->from->first_name;
        $last_name = $bot->message()->from->last_name;
        $language_code = $bot->message()->from->language_code;
        $created_at = User::whereTelegramUserId($telegram_user_id)->value('created_at');
        $user_number = User::whereTelegramUserId($telegram_user_id)->value('id');

        if (User::whereTelegramUserId($telegram_user_id)->exists()) {
            $bot->sendMessage
            ("You are already registered in system." . "\n" . "Registration date: $created_at. User number: $user_number");
        } else {
            User::create([
                'username' => $username,
                'firstname' => $first_name,
                'lastname' => $last_name,
                'telegram_user_id' => $telegram_user_id,
                'language_code' => $language_code,
            ]);
            $user_number = User::whereTelegramUserId($telegram_user_id)->value('id');
            $bot->sendMessage("Welcome to today_is bot." . "\n" . "You are user number $user_number" . "\n" .
                "For correct work in different timezones, push the button bellow for provide your location",
                ['reply_markup' => ReplyKeyboardMarkup::make(resize_keyboard: true, one_time_keyboard: true)
                    ->addRow(KeyboardButton::make('Registration', false, true))]);
        }
    }
}
