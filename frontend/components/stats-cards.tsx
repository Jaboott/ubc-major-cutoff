"use client"

import { Card, CardContent } from "@/components/ui/card"
import { TrendingUp, Users, Award, BarChart } from "lucide-react"
import { useEffect, useState } from "react"

interface StatsCardsProps {
    majorData: Record<string, { type: string; data: Array<{ year: string; gpa: number }> }>
    selectedMajor: string
}

function AnimatedCounter({ value, decimals = 0 }: { value: number; decimals?: number }) {
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

export function StatsCards({ majorData, selectedMajor }: StatsCardsProps) {
    // Calculate overall statistics
    const allMajors = Object.keys(majorData)
    const currentYear = "2024"

    // Get highest GPA major
    const highestGPAMajor = allMajors.reduce((highest, major) => {
        const currentGPA = majorData[major].data.find((d) => d.year === currentYear)?.gpa || 0
        const highestGPA = majorData[highest].data.find((d) => d.year === currentYear)?.gpa || 0
        return currentGPA > highestGPA ? major : highest
    }, allMajors[0])

    const highestGPA = majorData[highestGPAMajor].data.find((d) => d.year === currentYear)?.gpa || 0

    // Calculate average GPA across all majors
    const averageGPA =
        allMajors.reduce((sum, major) => {
            const gpa = majorData[major].data.find((d) => d.year === currentYear)?.gpa || 0
            return sum + gpa
        }, 0) / allMajors.length

    // Calculate average trend
    const averageTrend =
        allMajors.reduce((sum, major) => {
            const data = majorData[major].data
            const firstGPA = data[0].cutoff
            const lastGPA = data[data.length - 1].cutoff
            return sum + ((lastGPA - firstGPA) / firstGPA) * 100
        }, 0) / allMajors.length

    // Get current major stats
    const currentMajorData = majorData[selectedMajor]
    const currentMajorGPA = currentMajorData.data.find((d) => d.year === currentYear)?.gpa || 0

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <Card className="hover-lift animate-fade-in-up stagger-1 transition-all duration-300 group">
                <CardContent className="pt-6">
                    <div className="flex items-center justify-between">
                        <div className="space-y-1">
                            <p className="text-sm text-muted-foreground">Selected Major</p>
                            <p className="text-2xl font-bold text-foreground">
                                <AnimatedCounter value={currentMajorGPA} decimals={2} />
                            </p>
                            <p className="text-xs text-muted-foreground truncate">{selectedMajor}</p>
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
                            <p className="text-sm text-muted-foreground">Highest Cutoff</p>
                            <p className="text-2xl font-bold text-foreground">
                                <AnimatedCounter value={highestGPA} decimals={2} />
                            </p>
                            <p className="text-xs text-muted-foreground truncate">{highestGPAMajor}</p>
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
                            <p className="text-sm text-muted-foreground">Average GPA</p>
                            <p className="text-2xl font-bold text-foreground">
                                <AnimatedCounter value={averageGPA} decimals={2} />
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
                                +<AnimatedCounter value={averageTrend} decimals={1} />% avg trend
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
