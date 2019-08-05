package aoc2018.days

import kotlin.text.Regex

import aoc2018.foundation.parseInput
import aoc2018.foundation.numRegex

class Timestamp (
        val year: Int, 
        val month: Int, 
        val day: Int, 
        val hour: Int, 
        val min: Int, 
        _action: String
): Comparable<Timestamp> {
    val action = when (_action) {
        "falls asleep" -> Action.SLEEP
        "wakes up" -> Action.WAKE
        else -> {
            Action.SHIFT
        }
    }

    val guard = if (action == Action.SHIFT) {
        numRegex.find(_action)?.let { it.value.toInt() }
        ?: throw java.lang.IllegalStateException("Invalid action: $_action")
    } else null

    override fun toString(): String {
        return "Timestamp( year=$year, month=$month, day=$day, hour=$hour, min=$min, action=$action, guard=$guard"
    }

    override fun compareTo(other: Timestamp) = compareValuesBy(
        this, 
        other,
        compareBy(nullsFirst(), Timestamp::year)
            .thenBy(Timestamp::month)
            .thenBy(Timestamp::day)
            .thenBy(Timestamp::hour)
            .thenBy(Timestamp::min),
        { it }
    )

    companion object {
        val regex = Regex("""(?x)
            \[
                (?<year>\d+)-(?<month>\d+)-(?<day>\d+)
                \s+
                (?<hour>\d+):(?<min>\d+)
            \]
            \s+
            (?<action>wakes\s+up|falls\s+asleep|
                Guard\s+\#\d+\s+begins\s+shift)
        """)
    }

    enum class Action { SLEEP, WAKE, SHIFT } 
}


fun parseTimestamp(str: String): Timestamp? {
    return Timestamp.regex.matchEntire(str)?.let { match ->
        val groups = match.groups
        Timestamp(
            groups.get("year")!!.value.toInt(),
            groups.get("month")!!.value.toInt(),
            groups.get("day")!!.value.toInt(),
            groups.get("hour")!!.value.toInt(),
            groups.get("min")!!.value.toInt(),
            groups.get("action")!!.value
        )
    } ?: throw java.lang.IllegalStateException("No match: $str")
}


fun parseSchedule(filename: String?): MutableMap<Int, MutableMap<Int, Int>> {
    val timestamps = mutableListOf<Timestamp>()
    parseInput(filename) { timestamps.add(parseTimestamp(it)!!) }

    val guardSleep = mutableMapOf<Int, MutableMap<Int, Int>>()
    var curGuard: Int? = null
    var sleepStart: Int? = null
    timestamps.sorted().forEach { ts ->
        when (ts.action) {
            Timestamp.Action.SHIFT -> {
                curGuard = ts.guard
                sleepStart = 0
            }
            Timestamp.Action.WAKE -> {
                val curGuardSleep = guardSleep.getOrPut(curGuard!!) { mutableMapOf<Int, Int>() }
                (sleepStart!! until ts.min).forEach { min ->
                    curGuardSleep[min] = curGuardSleep.getOrDefault(min, 0) + 1
                }
            }
            Timestamp.Action.SLEEP -> sleepStart = ts.min
        }
    }

    return guardSleep
}

fun day4_1(filename: String?) {
    val guardSleep = parseSchedule(filename)

    val sleepiestGuard = guardSleep
        .mapValues { (_, sleep) -> sleep.values.sum() }
        .maxBy { it.value }
        ?.key

    val sleepiestMin = guardSleep[sleepiestGuard]
        ?.maxBy { it.value }
        ?.key
    
    if (sleepiestGuard != null && sleepiestMin != null) {
        println(sleepiestGuard*sleepiestMin)
    } else {
        println("Failed to find sleepiest guard/minute.")
    }
}

fun day4_2(filename: String?) {
    val guardSleep = parseSchedule(filename)
    val mostConsistent = guardSleep
        .mapValues { (_, sleep) -> sleep.maxBy { it.value }!! }
        .maxBy { (_, guardMax) -> guardMax.value }
        ?.let { (guard, guardMax) -> 
            guard * guardMax.key
        }

    mostConsistent?.let {
        println(mostConsistent)
    } ?: println("Failed to find most consistent guard/minute.")
}
