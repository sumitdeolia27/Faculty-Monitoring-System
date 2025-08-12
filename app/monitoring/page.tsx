"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Camera, Play, Square, RefreshCw, AlertTriangle, CheckCircle } from "lucide-react"
import Link from "next/link"

interface Detection {
  id: number
  name: string
  confidence: number
  timestamp: string
  camera: string
}

export default function LiveMonitoring() {
  const [isMonitoring, setIsMonitoring] = useState(true)
  const [detections, setDetections] = useState<Detection[]>([
    {
      id: 1,
      name: "Dr. Sarah Wilson",
      confidence: 0.94,
      timestamp: "09:15:23 AM",
      camera: "Main Entrance",
    },
    {
      id: 2,
      name: "Dr. Emma Davis",
      confidence: 0.89,
      timestamp: "09:14:12 AM",
      camera: "Faculty Lounge",
    },
    {
      id: 3,
      name: "Unknown Person",
      confidence: 0.67,
      timestamp: "09:13:45 AM",
      camera: "Corridor A",
    },
  ])

  const cameras = [
    { id: 1, name: "Main Entrance", status: "active", fps: 30 },
    { id: 2, name: "Faculty Lounge", status: "active", fps: 25 },
    { id: 3, name: "Corridor A", status: "active", fps: 30 },
    { id: 4, name: "Conference Room", status: "active", fps: 30 },
    { id: 5, name: "Library", status: "inactive", fps: 0 },
    { id: 6, name: "Cafeteria", status: "active", fps: 20 },
  ]

  // Simulate real-time detection updates
  useEffect(() => {
    if (isMonitoring) {
      const interval = setInterval(() => {
        const newDetection: Detection = {
          id: Date.now(),
          name: Math.random() > 0.7 ? "Dr. John Miller" : "Unknown Person",
          confidence: Math.random() * 0.3 + 0.7, // 0.7 to 1.0
          timestamp: new Date().toLocaleTimeString(),
          camera: cameras[Math.floor(Math.random() * cameras.length)].name,
        }
        setDetections((prev) => [newDetection, ...prev.slice(0, 9)]) // Keep last 10
      }, 3000)

      return () => clearInterval(interval)
    }
  }, [isMonitoring])

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-green-50 to-teal-100">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md shadow-lg border-b border-white/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <Link
                href="/"
                className="flex items-center text-blue-600 hover:text-blue-800 mr-6 transition-colors duration-200"
              >
                <div className="relative">
                  <div className="absolute inset-0 bg-gradient-to-r from-green-600 to-teal-600 rounded-lg blur opacity-75"></div>
                  <Camera className="relative h-6 w-6 mr-2 text-white bg-gradient-to-r from-green-600 to-teal-600 p-1 rounded-lg" />
                </div>
                <span className="font-semibold">← Back to Dashboard</span>
              </Link>
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
                  Live Monitoring
                </h1>
                <p className="text-sm text-gray-600 font-medium">Real-time faculty detection and verification</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Badge
                variant="outline"
                className={isMonitoring ? "text-green-600 border-green-300" : "text-gray-600 border-gray-300"}
              >
                <div className={`w-2 h-2 rounded-full mr-2 ${isMonitoring ? "bg-green-500" : "bg-gray-400"}`}></div>
                {isMonitoring ? "Monitoring Active" : "Monitoring Stopped"}
              </Badge>
              <Button onClick={() => setIsMonitoring(!isMonitoring)} variant={isMonitoring ? "destructive" : "default"}>
                {isMonitoring ? (
                  <>
                    <Square className="h-4 w-4 mr-2" />
                    Stop Monitoring
                  </>
                ) : (
                  <>
                    <Play className="h-4 w-4 mr-2" />
                    Start Monitoring
                  </>
                )}
              </Button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Camera Grid */}
          <div className="lg:col-span-2">
            <Card className="mb-6 shadow-xl border-0 overflow-hidden">
              <CardHeader className="bg-gradient-to-r from-green-600 to-teal-600 text-white">
                <CardTitle className="text-xl font-bold">Camera Feeds</CardTitle>
                <CardDescription className="text-green-100">
                  Live video streams with AI detection overlay
                </CardDescription>
              </CardHeader>
              <CardContent className="p-6">
                <div className="grid grid-cols-2 gap-6">
                  {cameras.map((camera) => (
                    <div key={camera.id} className="relative group">
                      <div className="aspect-video bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 rounded-xl overflow-hidden shadow-lg group-hover:shadow-2xl transition-all duration-300">
                        <div className="w-full h-full bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center">
                          <div className="text-white text-center">
                            <Camera className="h-12 w-12 mx-auto mb-2 opacity-50" />
                            <p className="text-sm font-medium">{camera.name}</p>
                            {camera.status === "active" && <p className="text-xs text-green-400">{camera.fps} FPS</p>}
                          </div>
                        </div>
                        {/* Detection Overlay */}
                        {camera.status === "active" && isMonitoring && (
                          <div className="absolute top-2 left-2">
                            <div className="bg-red-500 text-white px-2 py-1 rounded text-xs font-medium">● REC</div>
                          </div>
                        )}
                        {/* Status Badge */}
                        <div className="absolute top-2 right-2">
                          <Badge className={camera.status === "active" ? "bg-green-500" : "bg-gray-500"}>
                            {camera.status}
                          </Badge>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Detection Log */}
          <div>
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  Recent Detections
                  <Button size="sm" variant="outline" onClick={() => setDetections([])}>
                    <RefreshCw className="h-4 w-4" />
                  </Button>
                </CardTitle>
                <CardDescription>Latest AI detection results</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4 max-h-96 overflow-y-auto">
                  {detections.map((detection) => (
                    <div key={detection.id} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                      <div className="flex-shrink-0">
                        {detection.name === "Unknown Person" ? (
                          <AlertTriangle className="h-5 w-5 text-orange-500" />
                        ) : (
                          <CheckCircle className="h-5 w-5 text-green-500" />
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900 truncate">{detection.name}</p>
                        <p className="text-xs text-gray-500">
                          {detection.camera} • {detection.timestamp}
                        </p>
                        <div className="flex items-center mt-1">
                          <div className="flex-1 bg-gray-200 rounded-full h-1.5">
                            <div
                              className="bg-blue-600 h-1.5 rounded-full"
                              style={{ width: `${detection.confidence * 100}%` }}
                            />
                          </div>
                          <span className="text-xs text-gray-500 ml-2">{Math.round(detection.confidence * 100)}%</span>
                        </div>
                      </div>
                    </div>
                  ))}
                  {detections.length === 0 && (
                    <div className="text-center py-8 text-gray-500">
                      <Camera className="h-8 w-8 mx-auto mb-2 opacity-50" />
                      <p className="text-sm">No recent detections</p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Processing Status */}
            <Card className="mt-6">
              <CardHeader>
                <CardTitle>Processing Pipeline</CardTitle>
                <CardDescription>ML model performance metrics</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">OpenCV Frame Capture</span>
                  <Badge className="bg-green-100 text-green-800">30 FPS</Badge>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">YOLOv8 Face Detection</span>
                  <Badge className="bg-green-100 text-green-800">12ms</Badge>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">DeepFace Verification</span>
                  <Badge className="bg-green-100 text-green-800">45ms</Badge>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Total Latency</span>
                  <Badge className="bg-blue-100 text-blue-800">65ms</Badge>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  )
}
