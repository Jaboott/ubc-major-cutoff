"use client"

import {useState, useEffect} from "react"
import {Search} from "lucide-react"
import {Input} from "@/components/ui/input"
import {Select, SelectContent, SelectItem, SelectTrigger, SelectValue} from "@/components/ui/select"
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card"
import {GPAChart} from "@/components/gpa-chart"
import {StatsCards} from "@/components/stats-cards"
import {DetailedDataTable} from "@/components/detailed-data-table"

type MajorData = { name: string, statistics: any[] }
type AvailableMajor = { name: string, uids: number[] }

export default function GPACutoffPage() {
    const [searchQuery, setSearchQuery] = useState("")
    const [selectedDomestic, setSelectedDomestic] = useState<boolean>(true)
    const [selectedMajor, setSelectedMajor] = useState<string>("")
    const [isLoaded, setIsLoaded] = useState(false)

    const [majorData, setMajorData] = useState<MajorData>({name: "", statistics: []})
    const [availableMajors, setAvailableMajors] = useState<AvailableMajor[]>([])
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        async function fetchInitialData() {
            setIsLoading(true)
            try {
                const majorsResponse = await fetch("http://127.0.0.1:5000/api/majors")
                const majorsJson = await majorsResponse.json()
                const majorsMap = new Map()

                majorsJson.data.forEach((major: {name: string, uid: number}) => {
                    const arr = majorsMap.get(major.name) || [];
                    arr.push(major.uid);
                    majorsMap.set(major.name, arr);
                })

                setAvailableMajors(Array.from(majorsMap.keys()).map((key: string) => {
                    return {name: key, uids: majorsMap.get(key)}
                }))

                const averageCutoffResponse = await fetch("http://127.0.0.1:5000/api/average-cutoffs")
                const averageCutoffJson = await averageCutoffResponse.json()
                setMajorData({name: "average", statistics: averageCutoffJson.data})
                setSelectedMajor("Average Cutoff")
            } catch (error) {
                console.error("Failed to fetch initial data:", error)
            } finally {
                setIsLoading(false)
                setIsLoaded(true)
            }
        }

        fetchInitialData()
    }, [])

    useEffect(() => {
        if (!selectedMajor || selectedMajor === "Average Cutoff") {
            return
        }

        async function fetchAdmissionStats() {
            setIsLoading(true)
            try {
                const admissionStats = []
                const uids = availableMajors.find(m => m.name === selectedMajor)?.uids || []

                for (const id of uids) {
                    const response = await fetch(`http://127.0.0.1:5000/api/admission/${id}`)
                    const admission = await response.json()
                    admissionStats.push(...admission.data)
                }

                setMajorData({
                    name: selectedMajor,
                    statistics: admissionStats
                })

            } catch (error) {
                console.error("Failed to fetch initial data:", error)
            } finally {
                setIsLoading(false)
                setIsLoaded(true)
            }
        }

        fetchAdmissionStats()
    }, [selectedMajor])

    const filteredMajors = availableMajors.filter((availableMajors) => {
        const name = availableMajors.name
        const statistics: any = majorData.statistics
        if (!statistics) return false

        return name.toLowerCase().includes(searchQuery.toLowerCase())
    })

    const currentMajorData: any = majorData.statistics.filter((data: any) => {
        if (data.domestic === undefined) {
            return true
        }
        return data.domestic === selectedDomestic
    })

    if (isLoading || !currentMajorData) {
        return (
            <main className="min-h-screen bg-background flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"/>
                    <p className="text-muted-foreground">Loading major data...</p>
                </div>
            </main>
        )
    }

    return (
        <main className="min-h-screen bg-background relative overflow-hidden">
            <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
                <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary/5 rounded-full blur-3xl animate-float"/>
                <div
                    className="absolute bottom-0 right-1/4 w-96 h-96 bg-accent/5 rounded-full blur-3xl animate-float"
                    style={{animationDelay: "1s"}}
                />
            </div>

            <div className="container mx-auto px-4 py-8 md:py-12">
                <div className={`mb-8 text-center relative ${isLoaded ? "animate-fade-in-up" : "opacity-0"}`}>
                    <h1 className="text-4xl font-bold tracking-tight text-foreground mb-3 text-balance">
                        Major GPA Cutoff Analysis
                    </h1>
                    <p className="text-lg text-muted-foreground text-balance">
                        Explore admission GPA requirements across different majors and years
                    </p>
                </div>

                {/*<div className={isLoaded ? "" : "opacity-0"}>*/}
                {/*    <StatsCards majorData={majorData.statistics} selectedMajor={majorData.name} />*/}
                {/*</div>*/}

                <div className={`mb-8 max-w-4xl mx-auto ${isLoaded ? "animate-fade-in-up stagger-2" : "opacity-0"}`}>
                    <Card>
                        <CardHeader>
                            <CardTitle className="text-xl">Search Majors</CardTitle>
                            <CardDescription>Find cutoff data for specific majors</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="flex flex-col md:flex-row gap-4">
                                <div className="flex-1 relative">
                                    <Search
                                        className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground"/>
                                    <Input
                                        type="text"
                                        placeholder="Search for a major..."
                                        value={searchQuery}
                                        onChange={(e) => setSearchQuery(e.target.value)}
                                        className="pl-10"
                                    />
                                </div>

                                <Select value={selectedDomestic ? "all" : "international"}
                                        onValueChange={(val) => setSelectedDomestic(val === "all")}>
                                    <SelectTrigger className="w-full md:w-[200px]">
                                        <SelectValue placeholder="Student type"/>
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="all">All Students</SelectItem>
                                        <SelectItem value="international">International</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>

                            {searchQuery && (
                                <div className="pt-2">
                                    <p className="text-sm text-muted-foreground mb-2">
                                        {filteredMajors.length} {filteredMajors.length === 1 ? "result" : "results"} found
                                    </p>
                                    <div className="flex flex-wrap gap-2">
                                        {filteredMajors.map((availableMajor) => (
                                            <button
                                                key={availableMajor.name}
                                                onClick={() => {
                                                    setSelectedMajor(availableMajor.name)
                                                    setSearchQuery("")
                                                }}
                                                className="px-3 py-1.5 text-sm rounded-md bg-secondary hover:bg-accent hover:text-accent-foreground transition-colors"
                                            >
                                                {availableMajor.name}
                                            </button>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </CardContent>
                    </Card>
                </div>

                <div className={`max-w-5xl mx-auto mb-8 ${isLoaded ? "animate-scale-in stagger-3" : "opacity-0"}`}>
                    <GPAChart majorName={selectedMajor} data={currentMajorData} />
                </div>

                <div className={`max-w-5xl mx-auto ${isLoaded ? "animate-fade-in-up stagger-4" : "opacity-0"}`}>
                    <DetailedDataTable
                        majorName={selectedMajor}
                        isDomestic={selectedDomestic}
                        data={currentMajorData}
                    />
                </div>
            </div>
        </main>
    )
}
