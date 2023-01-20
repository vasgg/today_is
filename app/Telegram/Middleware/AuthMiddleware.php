<?php

namespace App\Telegram\Middleware;

use App\Models\User;
use SergiX44\Nutgram\Nutgram;

class AuthMiddleware
{
    public function __invoke(Nutgram $bot, $next): void
    {
        $userId = $bot->userId();
        $isUserRegistered = User::whereUserId($userId)->exists();
        $bot->setData('inDB', $isUserRegistered);
        $next($bot);
    }
}
