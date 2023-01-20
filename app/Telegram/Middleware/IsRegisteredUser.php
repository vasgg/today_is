<?php

namespace App\Telegram\Middleware;

use SergiX44\Nutgram\Nutgram;

class IsRegisteredUser
{
    public function __invoke(Nutgram $bot, $next): void
    {
        if ($bot->user()?->id === 123456789) {
            return;
        }

        $next($bot);
    }
}
