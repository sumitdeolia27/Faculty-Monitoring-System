import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Camera, Users, AlertTriangle, CheckCircle, Clock, Settings, TrendingUp, Shield, Zap } from "lucide-react"
import Link from "next/link"

export default function Dashboard() {
  const stats = [
    {
      title: "Total Faculty",
      value: "24",
      icon: Users,
      color: "text-blue-600",
      bgColor: "bg-gradient-to-br from-blue-50 to-blue-100",
      change: "+2 this month",
      changeColor: "text-green-600",
    },
    {
      title: "Present Today",
      value: "18",
      icon: CheckCircle,
      color: "text-green-600",
      bgColor: "bg-gradient-to-br from-green-50 to-green-100",
      change: "75% attendance",
      changeColor: "text-green-600",
    },
    {
      title: "Active Cameras",
      value: "8",
      icon: Camera,
      color: "text-purple-600",
      bgColor: "bg-gradient-to-br from-purple-50 to-purple-100",
      change: "All operational",
      changeColor: "text-green-600",
    },
    {
      title: "Alerts Today",
      value: "3",
      icon: AlertTriangle,
      color: "text-red-600",
      bgColor: "bg-gradient-to-br from-red-50 to-red-100",
      change: "-2 from yesterday",
      changeColor: "text-green-600",
    },
  ]

  const recentActivity = [
    { name: "Dr. Sarah Wilson", action: "Arrived", time: "09:15 AM", status: "present", avatar: "SW" },
    { name: "Prof. John Miller", action: "Left", time: "08:45 AM", status: "absent", avatar: "JM" },
    { name: "Dr. Emma Davis", action: "Arrived", time: "08:30 AM", status: "present", avatar: "ED" },
    { name: "Prof. Michael Brown", action: "Alert - Not detected", time: "08:00 AM", status: "alert", avatar: "MB" },
  ]

  const systemMetrics = [
    { label: "Detection Accuracy", value: "94.2%", icon: TrendingUp, color: "text-green-600" },
    { label: "System Uptime", value: "99.8%", icon: Shield, color: "text-blue-600" },
    { label: "Processing Speed", value: "65ms", icon: Zap, color: "text-purple-600" },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md shadow-lg border-b border-white/20 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl blur opacity-75"></div>
                <Camera className="relative h-10 w-10 text-white bg-gradient-to-r from-blue-600 to-purple-600 p-2 rounded-xl" />
              </div>
              <div className="ml-4">
                <h1 className="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
                  Faculty Monitoring System
                </h1>
                <p className="text-sm text-gray-600 font-medium">Real-time presence detection & intelligent alerts</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Badge variant="outline" className="text-green-600 border-green-300 bg-green-50 px-4 py-2 font-medium">
                <div className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></div>
                System Online
              </Badge>
              <Link href="/settings">
                <Button
                  variant="outline"
                  size="sm"
                  className="hover:bg-gray-50 transition-all duration-200 hover:scale-105 bg-transparent"
                >
                  <Settings className="h-4 w-4 mr-2" />
                  Settings
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
            <Card
              key={index}
              className="group hover:shadow-xl transition-all duration-300 hover:-translate-y-1 border-0 shadow-lg"
            >
              <CardContent className="p-6">
                <div className={`${stat.bgColor} rounded-2xl p-4 mb-4`}>
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-semibold text-gray-600 mb-1">{stat.title}</p>
                      <p className="text-3xl font-bold text-gray-900">{stat.value}</p>
                      <p className={`text-xs font-medium ${stat.changeColor} mt-1`}>{stat.change}</p>
                    </div>
                    <div className={`${stat.color} bg-white rounded-xl p-3 shadow-md`}>
                      <stat.icon className="h-8 w-8" />
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Recent Activity */}
          <div className="lg:col-span-2">
            <Card className="shadow-xl border-0 overflow-hidden">
              <CardHeader className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
                <CardTitle className="text-xl font-bold">Recent Activity</CardTitle>
                <CardDescription className="text-blue-100">Latest faculty presence updates</CardDescription>
              </CardHeader>
              <CardContent className="p-0">
                <div className="divide-y divide-gray-100">
                  {recentActivity.map((activity, index) => (
                    <div key={index} className="p-6 hover:bg-gray-50 transition-colors duration-200">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                          <div
                            className={`w-12 h-12 rounded-full flex items-center justify-center text-white font-bold text-sm shadow-lg ${
                              activity.status === "present"
                                ? "bg-gradient-to-br from-green-400 to-green-600"
                                : activity.status === "absent"
                                  ? "bg-gradient-to-br from-gray-400 to-gray-600"
                                  : "bg-gradient-to-br from-red-400 to-red-600"
                            }`}
                          >
                            {activity.avatar}
                          </div>
                          <div>
                            <p className="font-semibold text-gray-900">{activity.name}</p>
                            <p className="text-sm text-gray-600">{activity.action}</p>
                          </div>
                        </div>
                        <div className="flex items-center text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded-full">
                          <Clock className="h-4 w-4 mr-1" />
                          {activity.time}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <Card className="shadow-xl border-0 overflow-hidden">
              <CardHeader className="bg-gradient-to-r from-purple-600 to-pink-600 text-white">
                <CardTitle className="text-lg font-bold">Quick Actions</CardTitle>
                <CardDescription className="text-purple-100">System management tools</CardDescription>
              </CardHeader>
              <CardContent className="p-6 space-y-3">
                <Link href="/faculty" className="block">
                  <Button
                    className="w-full justify-start bg-gradient-to-r from-blue-50 to-blue-100 text-blue-700 border-blue-200 hover:from-blue-100 hover:to-blue-200 transition-all duration-200 hover:scale-105"
                    variant="outline"
                  >
                    <Users className="h-4 w-4 mr-2" />
                    Manage Faculty
                  </Button>
                </Link>
                <Link href="/monitoring" className="block">
                  <Button
                    className="w-full justify-start bg-gradient-to-r from-green-50 to-green-100 text-green-700 border-green-200 hover:from-green-100 hover:to-green-200 transition-all duration-200 hover:scale-105"
                    variant="outline"
                  >
                    <Camera className="h-4 w-4 mr-2" />
                    Live Monitoring
                  </Button>
                </Link>
                <Link href="/alerts" className="block">
                  <Button
                    className="w-full justify-start bg-gradient-to-r from-red-50 to-red-100 text-red-700 border-red-200 hover:from-red-100 hover:to-red-200 transition-all duration-200 hover:scale-105"
                    variant="outline"
                  >
                    <AlertTriangle className="h-4 w-4 mr-2" />
                    View Alerts
                  </Button>
                </Link>
              </CardContent>
            </Card>

            {/* System Metrics */}
            <Card className="shadow-xl border-0 overflow-hidden">
              <CardHeader className="bg-gradient-to-r from-green-600 to-teal-600 text-white">
                <CardTitle className="text-lg font-bold">System Metrics</CardTitle>
                <CardDescription className="text-green-100">Performance indicators</CardDescription>
              </CardHeader>
              <CardContent className="p-6 space-y-4">
                {systemMetrics.map((metric, index) => (
                  <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded-xl">
                    <div className="flex items-center space-x-3">
                      <metric.icon className={`h-5 w-5 ${metric.color}`} />
                      <span className="text-sm font-medium text-gray-700">{metric.label}</span>
                    </div>
                    <Badge className="bg-white text-gray-800 font-bold">{metric.value}</Badge>
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* System Status */}
            <Card className="shadow-xl border-0 overflow-hidden">
              <CardHeader className="bg-gradient-to-r from-indigo-600 to-blue-600 text-white">
                <CardTitle className="text-lg font-bold">ML Pipeline Status</CardTitle>
                <CardDescription className="text-indigo-100">Processing components</CardDescription>
              </CardHeader>
              <CardContent className="p-6 space-y-4">
                <div className="flex justify-between items-center p-3 bg-green-50 rounded-xl border border-green-200">
                  <span className="text-sm font-medium text-gray-700">OpenCV Capture</span>
                  <Badge className="bg-green-500 text-white animate-pulse">Active</Badge>
                </div>
                <div className="flex justify-between items-center p-3 bg-green-50 rounded-xl border border-green-200">
                  <span className="text-sm font-medium text-gray-700">YOLOv8 Detection</span>
                  <Badge className="bg-green-500 text-white animate-pulse">Running</Badge>
                </div>
                <div className="flex justify-between items-center p-3 bg-green-50 rounded-xl border border-green-200">
                  <span className="text-sm font-medium text-gray-700">DeepFace Verification</span>
                  <Badge className="bg-green-500 text-white animate-pulse">Online</Badge>
                </div>
                <div className="flex justify-between items-center p-3 bg-green-50 rounded-xl border border-green-200">
                  <span className="text-sm font-medium text-gray-700">Alert System</span>
                  <Badge className="bg-green-500 text-white animate-pulse">Ready</Badge>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  )
}
