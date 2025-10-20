import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card"
import {Table, TableBody, TableCell, TableHead, TableHeader, TableRow} from "@/components/ui/table"
import {Badge} from "@/components/ui/badge"
import {TrendingUp, TrendingDown, Users, UserX, UserCheck} from "lucide-react"

interface DetailedDataTableProps {
    majorName: string
    isDomestic: boolean
    data: any[]
}

export function DetailedDataTable({majorName, isDomestic, data}: DetailedDataTableProps) {
    data.forEach((data: any) => {
        data.min_grade = Number(data.min_grade)
        data.max_grade = Number(data.max_grade)
        data.initial_reject = Number(data.initial_reject)
        data.final_admit = Number(data.final_admit)
    })

    data.sort((a, b) => a.year - b.year)
    // Calculate totals and averages
    const totalInitialReject = data.reduce((sum, d) => sum + d.initial_reject, 0)
    const totalFinalAdmit = data.reduce((sum, d) => sum + d.final_admit, 0)
    const avgMinGrade = data.reduce((sum, d) => sum + d.min_grade, 0) / data.length

    return (
        <Card className="hover-lift transition-all duration-300">
            <CardHeader>
                <div className="flex items-start justify-between">
                    <div>
                        <CardTitle className="text-xl text-balance">Detailed Admission Statistics</CardTitle>
                        <CardDescription className="mt-1.5">
                            {majorName} • {isDomestic ? "All" : "International"} Students
                        </CardDescription>
                        <CardDescription className="mt-1.5 text-destructive">
                            Note: Some data may be incomplete, as recent sources no longer provide details available in past years
                        </CardDescription>
                    </div>
                    <Badge variant={isDomestic ? "default" : "secondary"} className="text-xs animate-pulse-glow">
                        {isDomestic ? "All" : "International"} Students
                    </Badge>
                </div>
            </CardHeader>
            <CardContent className="space-y-6">
                {/* Summary Cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="rounded-lg border bg-card p-4 hover-lift transition-all duration-300 group">
                        <div className="flex items-center gap-2 mb-2">
                            <UserX
                                className="h-4 w-4 text-destructive transition-transform duration-300 group-hover:scale-110"/>
                            <p className="text-sm font-medium text-muted-foreground">Total Initial Rejects</p>
                        </div>
                        <p className="text-2xl font-bold text-foreground">{totalInitialReject.toLocaleString()}</p>
                        <p className="text-xs text-muted-foreground mt-1">Across all years</p>
                    </div>

                    <div className="rounded-lg border bg-card p-4 hover-lift transition-all duration-300 group">
                        <div className="flex items-center gap-2 mb-2">
                            <UserCheck
                                className="h-4 w-4 text-accent transition-transform duration-300 group-hover:scale-110"/>
                            <p className="text-sm font-medium text-muted-foreground">Total Final Admits</p>
                        </div>
                        <p className="text-2xl font-bold text-foreground">{totalFinalAdmit.toLocaleString()}</p>
                        <p className="text-xs text-muted-foreground mt-1">Across all years</p>
                    </div>

                    <div className="rounded-lg border bg-card p-4 hover-lift transition-all duration-300 group">
                        <div className="flex items-center gap-2 mb-2">
                            <Users
                                className="h-4 w-4 text-chart-2 transition-transform duration-300 group-hover:scale-110"/>
                            <p className="text-sm font-medium text-muted-foreground">Avg Cutoff</p>
                        </div>
                        <p className="text-2xl font-bold text-foreground">{avgMinGrade.toFixed(2)}</p>
                        <p className="text-xs text-muted-foreground mt-1">Minimum accepted GPA</p>
                    </div>
                </div>

                {/* Data Table */}
                <div className="rounded-md border overflow-hidden">
                    <Table>
                        <TableHeader>
                            <TableRow className="bg-muted/50">
                                <TableHead className="font-semibold">Year</TableHead>
                                <TableHead className="font-semibold">Cutoff</TableHead>
                                <TableHead className="font-semibold">Max Grade</TableHead>
                                <TableHead className="font-semibold text-right">Initial Rejects</TableHead>
                                <TableHead className="font-semibold text-right">Final Admits</TableHead>
                                <TableHead className="font-semibold text-right">Accept Rate</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {data.map((row, index) => {
                                const acceptRate = (row.final_admit / (row.final_admit + row.initial_reject)) * 100
                                const prevRow = index > 0 ? data[index - 1] : null
                                const gpaTrend = prevRow ? row.min_grade - prevRow.min_grade : 0

                                return (
                                    <TableRow key={row.year}
                                              className="transition-colors duration-200 hover:bg-muted/50">
                                        <TableCell className="font-medium">{row.year}</TableCell>
                                        <TableCell>
                                            <div className="flex items-center gap-2">
                                                <span className="font-semibold">{row.min_grade.toFixed(2)}</span>
                                                {gpaTrend !== 0 && (
                                                    <span
                                                        className={`text-xs flex items-center gap-0.5 ${
                                                            gpaTrend > 0 ? "text-destructive" : "text-accent"
                                                        }`}
                                                    >
                            {gpaTrend > 0 ? <TrendingUp className="h-3 w-3"/> : <TrendingDown className="h-3 w-3"/>}
                                                        {Math.abs(gpaTrend).toFixed(2)}
                          </span>
                                                )}
                                            </div>
                                        </TableCell>
                                        <TableCell>
                                            <span
                                                className="text-muted-foreground">{row.max_grade !== 0 ? row.max_grade.toFixed(2) : ""}</span>
                                        </TableCell>
                                        <TableCell className="text-right">
                                            <span
                                                className="text-destructive font-medium">{row.initial_reject !== 0 ? row.initial_reject.toLocaleString() : ""}</span>
                                        </TableCell>
                                        <TableCell className="text-right">
                                            <span
                                                className="text-accent font-medium">{row.final_admit !== 0 ? row.final_admit.toLocaleString() : ""}</span>
                                        </TableCell>
                                        <TableCell className="text-right">{
                                            !Number.isNaN(acceptRate) &&
                                            <Badge variant={acceptRate > 50 ? "default" : "secondary"}
                                                   className="font-mono text-xs">
                                                {acceptRate.toFixed(1)}%
                                            </Badge>
                                        }
                                        </TableCell>
                                    </TableRow>
                                )
                            })}
                        </TableBody>
                    </Table>
                </div>

                {/* Additional Insights */}
                <div className="rounded-lg bg-muted/30 p-4 space-y-2 relative overflow-hidden group">
                    <div
                        className="absolute inset-0 shimmer-effect opacity-0 group-hover:opacity-100 transition-opacity duration-500"/>
                    <p className="text-sm font-medium text-foreground relative z-10">Key Insights</p>
                    <ul className="text-sm text-muted-foreground space-y-1 list-disc list-inside relative z-10">
                        <li>
                            Major cutoff increased by{" "}
                            <span className="font-semibold text-foreground">
                {(data[data.length - 1].min_grade - data[0].min_grade).toFixed(2)}
              </span>{" "}
                            percent from {data[0].year} to {data[data.length - 1].year}
                        </li>
                        <li>
                            Average acceptance rate:{" "}
                            <span className="font-semibold text-foreground">
                {((s = data.reduce((a, d) => d.initial_reject && d.final_admit ? {
                    sum: a.sum + (d.final_admit / (d.final_admit + d.initial_reject)) * 100,
                    count: a.count + 1
                } : a, {sum: 0, count: 0})) => s.count ? s.sum / s.count : 0)().toFixed(2)}%
              </span>
                        </li>
                        <li>
                            Minimum cutoff ranges from{" "}
                            <span className="font-semibold text-foreground">
                {Math.min(...data.map((d) => d.min_grade)).toFixed(2)}
              </span>{" "}
                            to{" "}
                            <span className="font-semibold text-foreground">
                {Math.max(...data.map((d) => d.min_grade)).toFixed(2)}
              </span>
                        </li>
                    </ul>
                </div>
            </CardContent>
        </Card>
    )
}
