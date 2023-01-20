<?php

namespace App\Telegram\Handlers;

use App\Models\User;
use SergiX44\Nutgram\Nutgram;
use Illuminate\Support\Facades\Http;
use SergiX44\Nutgram\Telegram\Types\Keyboard\ReplyKeyboardRemove;

class LocationHandler
{
    public function __invoke(Nutgram $bot): void
    {
        $bot->onLocation(function (Nutgram $bot) {
            $telegram_user_id = $bot->message()->from->id;
            $longitude = $bot->message()->location->longitude;
            $latitude = $bot->message()->location->latitude;
            $url = "http://api.geonames.org/timezoneJSON?lat=$latitude&lng=$longitude&username=vas1stdas";
            $response = Http::get($url);
            $countryCode = $response['countryCode'];
            $utcOffset = $response['gmtOffset'];
            $timezoneId = $response['timezoneId'];
            $countryName = $response['countryName'];
            $bot->sendMessage("Your location is: $longitude, $latitude" . "\n" .
                "Country: $countryName ($countryCode)" . "\n" .
                "Timezone: $timezoneId (UTC offset: $utcOffset)" . "\n",
                ['reply_markup' => ReplyKeyboardRemove::make(true)]);
            User::whereUserId($telegram_user_id)->update(['utc_offset' => $utcOffset]);
            $bot->close();
        });
    }
}
