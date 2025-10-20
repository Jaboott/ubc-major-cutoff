"use client"

import { Card, CardContent } from "@/components/ui/card"
import { TrendingUp, Users, Award, BarChart } from "lucide-react"
import { useEffect, useState } from "react"
import {MajorData} from "@/app/page";

interface StatsCardsProps {
    majorData: MajorData
    availableMajors: any[]
    averageData: MajorData
    maxCutoff: {name: string, stats: any}
}

function AnimatedCounter({ value, decimals = 0 }: { value: number; decimals?: number }) {
    value = Number(value)
    const [count, setCount] = useState(0)

    useEffect(() => {
        const duration = 1000
        const steps = 60
        const increment = value / steps
        let current = 0

        const timer = setInterval(() => {
            current += increment
            if (current >= value) {
                setCount(value)
                clearInterval(timer)
            } else {
                setCount(current)
            }
        }, duration / steps)

        return () => clearInterval(timer)
    }, [value])

    return <span>{count.toFixed(decimals)}</span>
}

export function StatsCards({ majorData, availableMajors, averageData, maxCutoff }: StatsCardsProps) {
    const sortedMajorStats = majorData.statistics.sort((a, b) => a.year - b.year)
    const sortedAverageData = averageData.statistics.sort((a, b) => a.year - b.year)

    // Calculate overall statistics
    const allMajors = Object.keys(availableMajors)

    // Get highest Cutoff major
    const highestCutoffMajor = maxCutoff.name
    const highestCutoff = maxCutoff.stats.min_grade

    // Calculate average Cutoff across all majors
    const averageCutoff = sortedAverageData[sortedAverageData.length - 1].min_grade

    // Calculate average trend
    const averageTrend = sortedAverageData[sortedAverageData.length - 1].min_grade - sortedAverageData[sortedAverageData.length - 2].min_grade

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <Card className="hover-lift animate-fade-in-up stagger-1 transition-all duration-300 group">
                <CardContent className="pt-6">
                    <div className="flex items-center justify-between">
                        <div className="space-y-1">
                            <p className="text-sm text-muted-foreground">Selected Major ({sortedMajorStats[sortedMajorStats.length - 1].year})</p>
                            <p className="text-2xl font-bold text-foreground">
                                <AnimatedCounter value={sortedMajorStats[sortedMajorStats.length-1].min_grade} decimals={2} />
                            </p>
                            <p className="text-xs text-muted-foreground truncate">{majorData.name}</p>
                        </div>
                        <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center transition-all duration-300 group-hover:scale-110 group-hover:bg-primary/20">
                            <Award className="h-6 w-6 text-primary transition-transform duration-300 group-hover:rotate-12" />
                        </div>
                    </div>
                </CardContent>
            </Card>

            <Card className="hover-lift animate-fade-in-up stagger-2 transition-all duration-300 group">
                <CardContent className="pt-6">
                    <div className="flex items-center justify-between">
                        <div className="space-y-1">
                            <p className="text-sm text-muted-foreground">Highest Cutoff ({maxCutoff.stats.year})</p>
                            <p className="text-2xl font-bold text-foreground">
                                <AnimatedCounter value={highestCutoff} decimals={2} />
                            </p>
                            <p className="text-xs text-muted-foreground truncate">{highestCutoffMajor}</p>
                        </div>
                        <div className="h-12 w-12 rounded-full bg-accent/10 flex items-center justify-center transition-all duration-300 group-hover:scale-110 group-hover:bg-accent/20">
                            <TrendingUp className="h-6 w-6 text-accent transition-transform duration-300 group-hover:translate-y-[-2px]" />
                        </div>
                    </div>
                </CardContent>
            </Card>

            <Card className="hover-lift animate-fade-in-up stagger-3 transition-all duration-300 group">
                <CardContent className="pt-6">
                    <div className="flex items-center justify-between">
                        <div className="space-y-1">
                            <p className="text-sm text-muted-foreground">Average Cutoff ({sortedAverageData[sortedAverageData.length - 1].year})</p>
                            <p className="text-2xl font-bold text-foreground">
                                <AnimatedCounter value={averageCutoff} decimals={2} />
                            </p>
                            <p className="text-xs text-muted-foreground">Across all majors</p>
                        </div>
                        <div className="h-12 w-12 rounded-full bg-chart-2/10 flex items-center justify-center transition-all duration-300 group-hover:scale-110 group-hover:bg-chart-2/20">
                            <BarChart className="h-6 w-6 text-chart-2 transition-transform duration-300 group-hover:scale-110" />
                        </div>
                    </div>
                </CardContent>
            </Card>

            <Card className="hover-lift animate-fade-in-up stagger-4 transition-all duration-300 group">
                <CardContent className="pt-6">
                    <div className="flex items-center justify-between">
                        <div className="space-y-1">
                            <p className="text-sm text-muted-foreground">Total Majors</p>
                            <p className="text-2xl font-bold text-foreground">
                                <AnimatedCounter value={allMajors.length} decimals={0} />
                            </p>
                            <p className="text-xs text-accent">
                                Cutoff {averageTrend >= 0 ? "+" : ""}<AnimatedCounter value={averageTrend} decimals={1} />% from last year
                            </p>
                        </div>
                        <div className="h-12 w-12 rounded-full bg-chart-3/10 flex items-center justify-center transition-all duration-300 group-hover:scale-110 group-hover:bg-chart-3/20">
                            <Users className="h-6 w-6 text-chart-3 transition-transform duration-300 group-hover:scale-110" />
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
