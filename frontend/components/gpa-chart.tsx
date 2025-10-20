"use client"

import { Line, LineChart, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Tooltip } from "recharts"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ChartContainer } from "@/components/ui/chart"

interface GPAChartProps {
    majorName: string
    data: any[]
}

const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
        return (
            <div className="rounded-lg border bg-background p-3 shadow-lg">
                <p className="text-sm font-medium text-foreground mb-1">Year: {label}</p>
                <p className="text-sm text-muted-foreground">
                    Cutoff: <span className="font-semibold text-foreground">{payload[0].value.toFixed(2)}</span>
                </p>
            </div>
        )
    }
    return null
}

export function GPAChart({ majorName, data }: GPAChartProps) {
    const dataCopy = data.map(d => ({
        ...d,
        min_grade: Number(d.min_grade),
    }))

    dataCopy.sort((a, b) => a.year - b.year)
    const firstGPA = dataCopy[0].min_grade
    const lastGPA = dataCopy[dataCopy.length - 1].min_grade
    const startYear = dataCopy[0].year
    const currYear = dataCopy[dataCopy.length - 1].year

    return (
        <Card>
            <CardHeader>
                <div>
                    <CardTitle className="text-2xl text-balance">{majorName}</CardTitle>
                    <CardDescription className="mt-1.5">Cutoff Trends ({startYear} - {currYear})</CardDescription>
                </div>
            </CardHeader>
            <CardContent>
                <ChartContainer
                    config={{
                        gpa: {
                            label: "GPA Cutoff",
                            color: "hsl(var(--chart-1))",
                        },
                    }}
                    className="h-[400px] w-full"
                >
                    <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={dataCopy} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
                            <CartesianGrid strokeDasharray="3 3" className="stroke-border" />
                            <XAxis
                                dataKey="year"
                                className="text-xs"
                                tick={{ fill: "hsl(var(--muted-foreground))" }}
                                tickLine={{ stroke: "hsl(var(--border))" }}
                            />
                            <YAxis
                                domain={[0, 100]}
                                ticks={[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]}
                                className="text-xs"
                                tick={{ fill: "hsl(var(--muted-foreground))" }}
                                tickLine={{ stroke: "hsl(var(--border))" }}
                            />
                            <Tooltip
                                content={<CustomTooltip />}
                                cursor={{ stroke: "hsl(var(--muted-foreground))", strokeWidth: 1 }}
                            />
                            <Line
                                type="monotone"
                                dataKey="min_grade"
                                stroke="hsl(var(--chart-1))"
                                strokeWidth={3}
                                dot={{
                                    fill: "hsl(var(--chart-1))",
                                    strokeWidth: 2,
                                    r: 5,
                                    stroke: "hsl(var(--background))",
                                }}
                                activeDot={{
                                    r: 8,
                                    stroke: "hsl(var(--chart-1))",
                                    strokeWidth: 3,
                                    fill: "hsl(var(--background))",
                                }}
                            />
                        </LineChart>
                    </ResponsiveContainer>
                </ChartContainer>

                {/* Stats Summary */}
                <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="space-y-1">
                        <p className="text-sm text-muted-foreground">Current ({currYear})</p>
                        <p className="text-2xl font-bold text-foreground">{lastGPA.toFixed(2)}</p>
                    </div>
                    <div className="space-y-1">
                        <p className="text-sm text-muted-foreground">Starting ({startYear})</p>
                        <p className="text-2xl font-bold text-foreground">{firstGPA.toFixed(2)}</p>
                    </div>
                    <div className="space-y-1">
                        <p className="text-sm text-muted-foreground">Increase ({startYear} - {currYear}) </p>
                        <p className="text-2xl font-bold text-accent">+{(lastGPA - firstGPA).toFixed(2)}</p>
                    </div>
                    <div className="space-y-1">
                        <p className="text-sm text-muted-foreground">Average Cutoff</p>
                        <p className="text-2xl font-bold text-foreground">
                            {(dataCopy.reduce((sum, d) => sum + d.min_grade, 0) / dataCopy.length).toFixed(2)}
                        </p>
                    </div>
                </div>
            </CardContent>
        </Card>
    )
}
