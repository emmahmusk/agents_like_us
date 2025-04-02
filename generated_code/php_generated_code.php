<?php
namespace App\Services;
/**
 * Calculates the return on investment (ROI).
 *
 * @param float $investment The initial investment amount.
 * @param float $return The total return on the investment.
 * @return float The ROI as a percentage.  Returns 0 if investment is 0 to avoid division by zero.
 */
function calculateRoi(float $investment, float $return): float
{
    return $investment === 0 ? 0 : ($return / $investment) * 100;
}