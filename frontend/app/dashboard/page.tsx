'use client'

import { useEffect, useState } from 'react'
import api from '@/lib/api'
import { Input } from '@/components/ui/input'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";

import { Button } from '@/components/ui/button'

interface Event {
  id: number
  title: string
  location: string
  event_date: string
  available_tickets: number
  total_tickets: number
}

export default function DashboardPage() {
  const [search, setSearch] = useState('')
  const [events, setEvents] = useState<Event[]>([])
  const [loading, setLoading] = useState(true)

  const [selectedEvent, setSelectedEvent] = useState<Event>()
  const [open, setOpen] = useState(false)

  const openDialog = (event: Event) => {
    setSelectedEvent({ ...event })
    setOpen(true)
  }

  const handleSave = () => {
    if (!selectedEvent) return
    setEvents((prev) =>
      prev.map((e) => (e.id === selectedEvent.id ? selectedEvent : e))
    )
    setOpen(false)
  }

  const filteredData = events.filter((item) =>
    item.title.toLowerCase().includes(search.toLowerCase()) ||
    item.location.toLowerCase().includes(search.toLowerCase())
  )

  useEffect(() => {
    const fetchEvents = async () => {
      const token = localStorage.getItem('token')
      if (!token) {
        console.error('No token found')
        setLoading(false)
        return
      }

      try {
        const { data } = await api.get<Event[]>('/events/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        setEvents(data)
      } catch (error) {
        console.error('Error fetching events:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchEvents()
  }, [])

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Events Dashboard</h1>

      <Input
        placeholder="Search by title or location..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="max-w-sm"
      />

      <div className="overflow-hidden rounded-lg border border-gray-200 shadow-sm">
        <Table>
          <TableHeader className="bg-gray-100">
            <TableRow>
              <TableHead className="text-gray-700">Title</TableHead>
              <TableHead className="text-gray-700">Location</TableHead>
              <TableHead className="text-gray-700">Date</TableHead>
              <TableHead className="text-gray-700">Available Tickets</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredData.map((event, index) => (
              <TableRow
                key={event.id}
                className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50 cursor-pointer'}
                onClick={() => openDialog(event)}
              >
                <TableCell>{event.title}</TableCell>
                <TableCell>{event.location}</TableCell>
                <TableCell>{new Date(event.event_date).toLocaleString()}</TableCell>
                <TableCell>{event.available_tickets} / {event.total_tickets}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Event</DialogTitle>
          </DialogHeader>
          {selectedEvent && (
            <div className="space-y-4 mt-4">
              <Input
                value={selectedEvent.title}
                onChange={(e) =>
                  setSelectedEvent({ ...selectedEvent, title: e.target.value })
                }
                placeholder="Title"
              />
              <Input
                value={selectedEvent.location}
                onChange={(e) =>
                  setSelectedEvent({ ...selectedEvent, location: e.target.value })
                }
                placeholder="Location"
              />
            </div>
          )}
          <DialogFooter className="mt-4">
            <Button variant="outline" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleSave}>Save</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
