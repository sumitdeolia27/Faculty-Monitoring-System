"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Label } from "@/components/ui/label"
import { Camera, Plus, Search, Upload, User, Mail, Phone, Edit, Trash2 } from "lucide-react"
import Link from "next/link"

interface Faculty {
  id: number
  name: string
  email: string
  phone: string
  department: string
  status: "present" | "absent"
  lastSeen: string
  imageUploaded: boolean
}

export default function FacultyManagement() {
  const [searchTerm, setSearchTerm] = useState("")
  const [faculty, setFaculty] = useState<Faculty[]>([
    {
      id: 1,
      name: "Dr. Sarah Wilson",
      email: "s.wilson@university.edu",
      phone: "+1-234-567-8901",
      department: "Computer Science",
      status: "present",
      lastSeen: "09:15 AM",
      imageUploaded: true,
    },
    {
      id: 2,
      name: "Prof. John Miller",
      email: "j.miller@university.edu",
      phone: "+1-234-567-8902",
      department: "Mathematics",
      status: "absent",
      lastSeen: "Yesterday 5:30 PM",
      imageUploaded: true,
    },
    {
      id: 3,
      name: "Dr. Emma Davis",
      email: "e.davis@university.edu",
      phone: "+1-234-567-8903",
      department: "Physics",
      status: "present",
      lastSeen: "08:30 AM",
      imageUploaded: false,
    },
    {
      id: 4,
      name: "Prof. Michael Brown",
      email: "m.brown@university.edu",
      phone: "+1-234-567-8904",
      department: "Chemistry",
      status: "absent",
      lastSeen: "2 days ago",
      imageUploaded: true,
    },
  ])

  const filteredFaculty = faculty.filter(
    (member) =>
      member.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      member.department.toLowerCase().includes(searchTerm.toLowerCase()),
  )

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-purple-50 to-pink-100">
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
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg blur opacity-75"></div>
                  <Camera className="relative h-6 w-6 mr-2 text-white bg-gradient-to-r from-blue-600 to-purple-600 p-1 rounded-lg" />
                </div>
                <span className="font-semibold">← Back to Dashboard</span>
              </Link>
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
                  Faculty Management
                </h1>
                <p className="text-sm text-gray-600 font-medium">Manage faculty profiles and reference images</p>
              </div>
            </div>
            <Dialog>
              <DialogTrigger asChild>
                <Button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 transition-all duration-200 hover:scale-105 shadow-lg">
                  <Plus className="h-4 w-4 mr-2" />
                  Add Faculty
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-md">
                <DialogHeader>
                  <DialogTitle>Add New Faculty Member</DialogTitle>
                  <DialogDescription>Add a new faculty member to the monitoring system</DialogDescription>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="name" className="text-right">
                      Name
                    </Label>
                    <Input id="name" className="col-span-3" />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="email" className="text-right">
                      Email
                    </Label>
                    <Input id="email" type="email" className="col-span-3" />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="phone" className="text-right">
                      Phone
                    </Label>
                    <Input id="phone" className="col-span-3" />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="department" className="text-right">
                      Department
                    </Label>
                    <Input id="department" className="col-span-3" />
                  </div>
                </div>
                <DialogFooter>
                  <Button type="submit">Add Faculty</Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search and Filters */}
        <div className="mb-6">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
            <Input
              placeholder="Search faculty by name or department..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 max-w-md"
            />
          </div>
        </div>

        {/* Faculty Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredFaculty.map((member) => (
            <Card
              key={member.id}
              className="group hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 border-0 shadow-lg overflow-hidden"
            >
              <CardHeader className="pb-4 bg-gradient-to-r from-blue-50 to-purple-50">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-14 h-14 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-lg shadow-lg">
                      {member.name
                        .split(" ")
                        .map((n) => n[0])
                        .join("")}
                    </div>
                    <div>
                      <CardTitle className="text-lg font-bold text-gray-900">{member.name}</CardTitle>
                      <CardDescription className="font-medium">{member.department}</CardDescription>
                    </div>
                  </div>
                  <Badge
                    variant={member.status === "present" ? "default" : "secondary"}
                    className={`${
                      member.status === "present"
                        ? "bg-gradient-to-r from-green-400 to-green-600 text-white shadow-md"
                        : "bg-gray-200 text-gray-700"
                    } px-3 py-1 font-semibold`}
                  >
                    {member.status}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <div className="flex items-center text-sm text-gray-600">
                    <Mail className="h-4 w-4 mr-2" />
                    {member.email}
                  </div>
                  <div className="flex items-center text-sm text-gray-600">
                    <Phone className="h-4 w-4 mr-2" />
                    {member.phone}
                  </div>
                  <div className="flex items-center text-sm text-gray-600">
                    <User className="h-4 w-4 mr-2" />
                    Last seen: {member.lastSeen}
                  </div>
                </div>

                <div className="flex items-center justify-between pt-4 border-t">
                  <div className="flex items-center space-x-2">
                    {member.imageUploaded ? (
                      <Badge className="bg-green-100 text-green-800">Reference Image: ✓</Badge>
                    ) : (
                      <Badge variant="outline" className="text-orange-600 border-orange-300">
                        No Image
                      </Badge>
                    )}
                  </div>
                  <div className="flex space-x-2">
                    <Button size="sm" variant="outline">
                      <Upload className="h-4 w-4" />
                    </Button>
                    <Button size="sm" variant="outline">
                      <Edit className="h-4 w-4" />
                    </Button>
                    <Button size="sm" variant="outline" className="text-red-600 hover:text-red-800 bg-transparent">
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {filteredFaculty.length === 0 && (
          <Card className="text-center py-12">
            <CardContent>
              <User className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No faculty found</h3>
              <p className="text-gray-600">Try adjusting your search criteria or add a new faculty member.</p>
            </CardContent>
          </Card>
        )}
      </main>
    </div>
  )
}
