<?php
/** @var SergiX44\Nutgram\Nutgram $bot */

use Illuminate\Support\Facades\DB;
use SergiX44\Nutgram\Nutgram;
use App\Models\User;
use App\Telegram\Commands\StartCommand;
use App\Telegram\Commands\SettingsCommand;
use App\Telegram\Handlers\LocationHandler;
/*
|--------------------------------------------------------------------------
| Nutgram Handlers
|--------------------------------------------------------------------------
|
| Here is where you can register telegram handlers for Nutgram. These
| handlers are loaded by the NutgramServiceProvider. Enjoy!
|
*/

$bot->onCommand('start', StartCommand::class);
$bot->onCommand('settings', SettingsCommand::class);
$bot->onLocation(LocationHandler::class);


// dd($chat_id);
//     return $bot->sendMessage('Hello, world!');
// })->description('The start command!');






