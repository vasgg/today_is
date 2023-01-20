<?php
/** @var SergiX44\Nutgram\Nutgram $bot */

use App\Telegram\Middleware\AuthMiddleware;
use App\Telegram\Commands\StartCommand;
use App\Telegram\Handlers\LocationHandler;

$bot->middleware(AuthMiddleware::class);
$bot->onCommand('start', StartCommand::class);
$bot->onLocation(LocationHandler::class);





//$bot->onCommand('settings', SettingsCommand::class);
// })->description('The start command!');






