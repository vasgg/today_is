<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Sanctum\HasApiTokens;

/**
 * @method static whereUserId(int $user_id)
 * @method static create(array $array)
 */
class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;

    protected $fillable = [
        'user_id',
        'firstname',
        'username',
        'lastname',
        'uts_offset',
        'language_code',
    ];

    public function records(): HasMany
    {
        return $this->hasMany(Record::class);
    }

}
