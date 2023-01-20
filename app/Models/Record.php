<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Record extends Model
{
    protected $fillable = [
        'event_name',
        'event_date',
    ];


    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class, 'id');
    }

}
