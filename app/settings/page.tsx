"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Separator } from "@/components/ui/separator"
import { Camera, Save, Settings, Bell, Database } from "lucide-react"
import Link from "next/link"

export default function SettingsPage() {
  const [settings, setSettings] = useState({
    // Detection Settings
    detectionThreshold: "0.8",
    faceDetectionModel: "yolov8",
    verificationModel: "deepface",
    processingInterval: "100",

    // Alert Settings
    alertsEnabled: true,
    emailNotifications: true,
    smsNotifications: false,
    alertThresholdHours: "2",
    highPriorityThreshold: "4",

    // Camera Settings
    defaultFPS: "30",
    recordingEnabled: true,
    recordingDuration: "24",
    compressionQuality: "75",

    // System Settings
    dataRetention: "30",
    backupEnabled: true,
    autoUpdate: true,
    debugMode: false,
  })

  const handleSettingChange = (key: string, value: any) => {
    setSettings((prev) => ({ ...prev, [key]: value }))
  }

  const handleSave = () => {
    // Here you would save settings to your backend
    console.log("Saving settings:", settings)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-indigo-50 to-blue-100">
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
                  <div className="absolute inset-0 bg-gradient-to-r from-indigo-600 to-blue-600 rounded-lg blur opacity-75"></div>
                  <Camera className="relative h-6 w-6 mr-2 text-white bg-gradient-to-r from-indigo-600 to-blue-600 p-1 rounded-lg" />
                </div>
                <span className="font-semibold">← Back to Dashboard</span>
              </Link>
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
                  System Settings
                </h1>
                <p className="text-sm text-gray-600 font-medium">Configure monitoring system parameters</p>
              </div>
            </div>
            <Button
              onClick={handleSave}
              className="bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-700 hover:to-blue-700 transition-all duration-200 hover:scale-105 shadow-lg"
            >
              <Save className="h-4 w-4 mr-2" />
              Save Changes
            </Button>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid gap-8">
          {/* AI & Detection Settings */}
          <Card className="shadow-xl border-0 overflow-hidden">
            <CardHeader className="bg-gradient-to-r from-indigo-600 to-blue-600 text-white">
              <CardTitle className="flex items-center text-xl font-bold">
                <Settings className="h-6 w-6 mr-3" />
                AI & Detection Settings
              </CardTitle>
              <CardDescription className="text-indigo-100">
                Configure machine learning models and detection parameters
              </CardDescription>
            </CardHeader>
            <CardContent className="p-8 space-y-8 bg-gradient-to-br from-white to-gray-50">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <Label htmlFor="detectionThreshold">Detection Confidence Threshold</Label>
                  <Input
                    id="detectionThreshold"
                    type="number"
                    min="0.1"
                    max="1.0"
                    step="0.1"
                    value={settings.detectionThreshold}
                    onChange={(e) => handleSettingChange("detectionThreshold", e.target.value)}
                  />
                  <p className="text-sm text-gray-500">Minimum confidence score for face detection (0.1 - 1.0)</p>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="processingInterval">Processing Interval (ms)</Label>
                  <Input
                    id="processingInterval"
                    type="number"
                    min="50"
                    max="1000"
                    value={settings.processingInterval}
                    onChange={(e) => handleSettingChange("processingInterval", e.target.value)}
                  />
                  <p className="text-sm text-gray-500">Time between frame processing cycles</p>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="faceDetectionModel">Face Detection Model</Label>
                  <Select
                    value={settings.faceDetectionModel}
                    onValueChange={(value) => handleSettingChange("faceDetectionModel", value)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="yolov8">YOLOv8 (Recommended)</SelectItem>
                      <SelectItem value="mtcnn">MTCNN</SelectItem>
                      <SelectItem value="opencv">OpenCV Haar Cascade</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="verificationModel">Face Verification Model</Label>
                  <Select
                    value={settings.verificationModel}
                    onValueChange={(value) => handleSettingChange("verificationModel", value)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="deepface">DeepFace (Recommended)</SelectItem>
                      <SelectItem value="facenet">FaceNet</SelectItem>
                      <SelectItem value="arcface">ArcFace</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Alert Settings */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Bell className="h-5 w-5 mr-2" />
                Alert & Notification Settings
              </CardTitle>
              <CardDescription>Configure alert thresholds and notification preferences</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label htmlFor="alertsEnabled">Enable Alerts</Label>
                  <p className="text-sm text-gray-500">Turn on/off the alert system</p>
                </div>
                <Switch
                  id="alertsEnabled"
                  checked={settings.alertsEnabled}
                  onCheckedChange={(checked) => handleSettingChange("alertsEnabled", checked)}
                />
              </div>

              <Separator />

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label htmlFor="emailNotifications">Email Notifications</Label>
                    <p className="text-sm text-gray-500">Send alerts via email</p>
                  </div>
                  <Switch
                    id="emailNotifications"
                    checked={settings.emailNotifications}
                    onCheckedChange={(checked) => handleSettingChange("emailNotifications", checked)}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label htmlFor="smsNotifications">SMS Notifications</Label>
                    <p className="text-sm text-gray-500">Send alerts via SMS</p>
                  </div>
                  <Switch
                    id="smsNotifications"
                    checked={settings.smsNotifications}
                    onCheckedChange={(checked) => handleSettingChange("smsNotifications", checked)}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="alertThresholdHours">Alert Threshold (Hours)</Label>
                  <Input
                    id="alertThresholdHours"
                    type="number"
                    min="1"
                    max="24"
                    value={settings.alertThresholdHours}
                    onChange={(e) => handleSettingChange("alertThresholdHours", e.target.value)}
                  />
                  <p className="text-sm text-gray-500">Hours of absence before triggering alert</p>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="highPriorityThreshold">High Priority Threshold (Hours)</Label>
                  <Input
                    id="highPriorityThreshold"
                    type="number"
                    min="2"
                    max="48"
                    value={settings.highPriorityThreshold}
                    onChange={(e) => handleSettingChange("highPriorityThreshold", e.target.value)}
                  />
                  <p className="text-sm text-gray-500">Hours of absence for high priority alert</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Camera Settings */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Camera className="h-5 w-5 mr-2" />
                Camera & Recording Settings
              </CardTitle>
              <CardDescription>Configure camera feeds and recording parameters</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <Label htmlFor="defaultFPS">Default Frame Rate (FPS)</Label>
                  <Select
                    value={settings.defaultFPS}
                    onValueChange={(value) => handleSettingChange("defaultFPS", value)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="15">15 FPS</SelectItem>
                      <SelectItem value="24">24 FPS</SelectItem>
                      <SelectItem value="30">30 FPS (Recommended)</SelectItem>
                      <SelectItem value="60">60 FPS</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="compressionQuality">Video Compression Quality (%)</Label>
                  <Input
                    id="compressionQuality"
                    type="number"
                    min="1"
                    max="100"
                    value={settings.compressionQuality}
                    onChange={(e) => handleSettingChange("compressionQuality", e.target.value)}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label htmlFor="recordingEnabled">Enable Recording</Label>
                    <p className="text-sm text-gray-500">Record video feeds</p>
                  </div>
                  <Switch
                    id="recordingEnabled"
                    checked={settings.recordingEnabled}
                    onCheckedChange={(checked) => handleSettingChange("recordingEnabled", checked)}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="recordingDuration">Recording Duration (Hours)</Label>
                  <Input
                    id="recordingDuration"
                    type="number"
                    min="1"
                    max="168"
                    value={settings.recordingDuration}
                    onChange={(e) => handleSettingChange("recordingDuration", e.target.value)}
                  />
                </div>
              </div>
            </CardContent>
          </Card>

          {/* System Settings */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Database className="h-5 w-5 mr-2" />
                System & Data Settings
              </CardTitle>
              <CardDescription>Configure system behavior and data management</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <Label htmlFor="dataRetention">Data Retention (Days)</Label>
                  <Input
                    id="dataRetention"
                    type="number"
                    min="1"
                    max="365"
                    value={settings.dataRetention}
                    onChange={(e) => handleSettingChange("dataRetention", e.target.value)}
                  />
                  <p className="text-sm text-gray-500">How long to keep detection logs and recordings</p>
                </div>

                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label htmlFor="backupEnabled">Enable Automatic Backup</Label>
                      <p className="text-sm text-gray-500">Backup data daily</p>
                    </div>
                    <Switch
                      id="backupEnabled"
                      checked={settings.backupEnabled}
                      onCheckedChange={(checked) => handleSettingChange("backupEnabled", checked)}
                    />
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label htmlFor="autoUpdate">Auto-Update Models</Label>
                      <p className="text-sm text-gray-500">Update AI models automatically</p>
                    </div>
                    <Switch
                      id="autoUpdate"
                      checked={settings.autoUpdate}
                      onCheckedChange={(checked) => handleSettingChange("autoUpdate", checked)}
                    />
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="space-y-0.5">
                      <Label htmlFor="debugMode">Debug Mode</Label>
                      <p className="text-sm text-gray-500">Enable detailed logging</p>
                    </div>
                    <Switch
                      id="debugMode"
                      checked={settings.debugMode}
                      onCheckedChange={(checked) => handleSettingChange("debugMode", checked)}
                    />
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
