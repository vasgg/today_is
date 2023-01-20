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
        $user_id = $bot->userId();
        $isUserRegistered = $bot->getData('inDB');

        switch ($isUserRegistered) {
            case true:
                $created_at = User::whereUserId($user_id)->value('created_at')->diffForHumans();
                $user_number = User::whereUserId($user_id)->value('id');
                $bot->sendMessage
                ("You are already registered in system $created_at. User number: $user_number");
                break;

            default:
                $username = $bot->message()->from->username;
                $first_name = $bot->message()->from->first_name;
                $last_name = $bot->message()->from->last_name;
                $language_code = $bot->message()->from->language_code;
                $user_number = User::whereUserId($user_id)->value('id');
                $bot->sendMessage("Welcome to today_is bot." . "\n" . "You are user number $user_number" . "\n" .
                    "For correct work in different timezones, push the button bellow for provide your location",
                    ['reply_markup' => ReplyKeyboardMarkup::make(resize_keyboard: true, one_time_keyboard: true)
                        ->addRow(KeyboardButton::make('Registration', false, true))]);
                User::create([
                    'username' => $username,
                    'firstname' => $first_name,
                    'lastname' => $last_name,
                    'user_id' => $user_id,
                    'language_code' => $language_code,
                ]);
                $user_number = User::whereUserId($user_id)->value('id');
                $bot->sendMessage("Welcome to today_is bot." . "\n" . "You are user number $user_number" . "\n" .
                    "For correct work in different timezones, push the button bellow for provide your location",
                    ['reply_markup' => ReplyKeyboardMarkup::make(resize_keyboard: true, one_time_keyboard: true)
                        ->addRow(KeyboardButton::make('Registration', false, true))]);
        }
    }
}
