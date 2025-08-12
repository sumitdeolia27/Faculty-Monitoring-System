"use client"

import { useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { AlertTriangle, Camera, Clock, Search, Bell, CheckCircle, XCircle, User } from "lucide-react"
import Link from "next/link"

interface Alert {
  id: number
  type: "absence" | "unknown_person" | "system_error"
  title: string
  description: string
  timestamp: string
  status: "active" | "resolved" | "dismissed"
  priority: "high" | "medium" | "low"
  facultyName?: string
  camera?: string
}

export default function AlertsPage() {
  const [searchTerm, setSearchTerm] = useState("")
  const [filterStatus, setFilterStatus] = useState("all")
  const [filterPriority, setFilterPriority] = useState("all")

  const [alerts, setAlerts] = useState<Alert[]>([
    {
      id: 1,
      type: "absence",
      title: "Faculty Not Detected",
      description: "Prof. Michael Brown has not been detected for 2 hours during scheduled office hours",
      timestamp: "2 hours ago",
      status: "active",
      priority: "high",
      facultyName: "Prof. Michael Brown",
      camera: "Main Entrance",
    },
    {
      id: 2,
      type: "unknown_person",
      title: "Unknown Person Detected",
      description: "Unrecognized individual detected in faculty lounge area",
      timestamp: "45 minutes ago",
      status: "active",
      priority: "medium",
      camera: "Faculty Lounge",
    },
    {
      id: 3,
      type: "system_error",
      title: "Camera Feed Lost",
      description: "Lost connection to Library camera feed",
      timestamp: "1 hour ago",
      status: "resolved",
      priority: "medium",
      camera: "Library",
    },
    {
      id: 4,
      type: "absence",
      title: "Extended Absence Alert",
      description: "Dr. Lisa Johnson has been absent for 3 consecutive days",
      timestamp: "3 hours ago",
      status: "dismissed",
      priority: "high",
      facultyName: "Dr. Lisa Johnson",
    },
    {
      id: 5,
      type: "unknown_person",
      title: "Unauthorized Access Attempt",
      description: "Multiple unknown persons detected in restricted area",
      timestamp: "Yesterday 6:30 PM",
      status: "resolved",
      priority: "high",
      camera: "Conference Room",
    },
  ])

  const filteredAlerts = alerts.filter((alert) => {
    const matchesSearch =
      alert.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      alert.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (alert.facultyName && alert.facultyName.toLowerCase().includes(searchTerm.toLowerCase()))

    const matchesStatus = filterStatus === "all" || alert.status === filterStatus
    const matchesPriority = filterPriority === "all" || alert.priority === filterPriority

    return matchesSearch && matchesStatus && matchesPriority
  })

  const getAlertIcon = (type: string) => {
    switch (type) {
      case "absence":
        return <User className="h-5 w-5 text-red-500" />
      case "unknown_person":
        return <AlertTriangle className="h-5 w-5 text-orange-500" />
      case "system_error":
        return <Camera className="h-5 w-5 text-blue-500" />
      default:
        return <Bell className="h-5 w-5 text-gray-500" />
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "high":
        return "bg-red-100 text-red-800 border-red-300"
      case "medium":
        return "bg-yellow-100 text-yellow-800 border-yellow-300"
      case "low":
        return "bg-blue-100 text-blue-800 border-blue-300"
      default:
        return "bg-gray-100 text-gray-800 border-gray-300"
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "active":
        return <AlertTriangle className="h-4 w-4 text-red-500" />
      case "resolved":
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case "dismissed":
        return <XCircle className="h-4 w-4 text-gray-500" />
      default:
        return <Bell className="h-4 w-4 text-gray-500" />
    }
  }

  const updateAlertStatus = (id: number, newStatus: "resolved" | "dismissed") => {
    setAlerts((prev) => prev.map((alert) => (alert.id === id ? { ...alert, status: newStatus } : alert)))
  }

  const activeAlertsCount = alerts.filter((alert) => alert.status === "active").length
  const highPriorityCount = alerts.filter((alert) => alert.priority === "high" && alert.status === "active").length

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-red-50 to-orange-100">
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
                  <div className="absolute inset-0 bg-gradient-to-r from-red-600 to-orange-600 rounded-lg blur opacity-75"></div>
                  <Camera className="relative h-6 w-6 mr-2 text-white bg-gradient-to-r from-red-600 to-orange-600 p-1 rounded-lg" />
                </div>
                <span className="font-semibold">← Back to Dashboard</span>
              </Link>
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
                  Alert Management
                </h1>
                <p className="text-sm text-gray-600 font-medium">Monitor and manage system alerts</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Badge variant="outline" className="text-red-600 border-red-300">
                <AlertTriangle className="h-4 w-4 mr-2" />
                {activeAlertsCount} Active Alerts
              </Badge>
              {highPriorityCount > 0 && <Badge className="bg-red-500">{highPriorityCount} High Priority</Badge>}
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Filters */}
        <div className="flex flex-col sm:flex-row gap-4 mb-6">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
            <Input
              placeholder="Search alerts..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
          <Select value={filterStatus} onValueChange={setFilterStatus}>
            <SelectTrigger className="w-48">
              <SelectValue placeholder="Filter by status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Status</SelectItem>
              <SelectItem value="active">Active</SelectItem>
              <SelectItem value="resolved">Resolved</SelectItem>
              <SelectItem value="dismissed">Dismissed</SelectItem>
            </SelectContent>
          </Select>
          <Select value={filterPriority} onValueChange={setFilterPriority}>
            <SelectTrigger className="w-48">
              <SelectValue placeholder="Filter by priority" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Priority</SelectItem>
              <SelectItem value="high">High</SelectItem>
              <SelectItem value="medium">Medium</SelectItem>
              <SelectItem value="low">Low</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Alerts List */}
        <div className="space-y-4">
          {filteredAlerts.map((alert) => (
            <Card
              key={alert.id}
              className={`group transition-all duration-300 hover:shadow-2xl hover:-translate-y-1 border-0 shadow-lg ${
                alert.status === "active" && alert.priority === "high"
                  ? "bg-gradient-to-r from-red-50 to-orange-50 border-l-4 border-l-red-500"
                  : "bg-white"
              }`}
            >
              <CardContent className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-4">
                    <div className="flex-shrink-0 mt-1">{getAlertIcon(alert.type)}</div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-3 mb-2">
                        <h3 className="text-lg font-medium text-gray-900">{alert.title}</h3>
                        <Badge variant="outline" className={getPriorityColor(alert.priority)}>
                          {alert.priority} priority
                        </Badge>
                        <div className="flex items-center text-sm text-gray-500">
                          {getStatusIcon(alert.status)}
                          <span className="ml-1 capitalize">{alert.status}</span>
                        </div>
                      </div>
                      <p className="text-gray-600 mb-3">{alert.description}</p>
                      <div className="flex items-center space-x-4 text-sm text-gray-500">
                        <div className="flex items-center">
                          <Clock className="h-4 w-4 mr-1" />
                          {alert.timestamp}
                        </div>
                        {alert.facultyName && (
                          <div className="flex items-center">
                            <User className="h-4 w-4 mr-1" />
                            {alert.facultyName}
                          </div>
                        )}
                        {alert.camera && (
                          <div className="flex items-center">
                            <Camera className="h-4 w-4 mr-1" />
                            {alert.camera}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                  {alert.status === "active" && (
                    <div className="flex space-x-2">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => updateAlertStatus(alert.id, "resolved")}
                        className="text-green-600 hover:text-green-800"
                      >
                        <CheckCircle className="h-4 w-4 mr-1" />
                        Resolve
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => updateAlertStatus(alert.id, "dismissed")}
                        className="text-gray-600 hover:text-gray-800"
                      >
                        <XCircle className="h-4 w-4 mr-1" />
                        Dismiss
                      </Button>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {filteredAlerts.length === 0 && (
          <Card className="text-center py-12">
            <CardContent>
              <Bell className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No alerts found</h3>
              <p className="text-gray-600">Try adjusting your search criteria or filters.</p>
            </CardContent>
          </Card>
        )}
      </main>
    </div>
  )
}
