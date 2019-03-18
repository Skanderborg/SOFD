using System;
using System.Net.Mail;
using DDay.iCal;
using DDay.iCal.Serialization.iCalendar;
using System.Net.Mime;

namespace Lib._365
{
    public class EmailService : IEmailService
    {
        public string SmtpHost { get; set; }

        public int SmtpPort { get; set; }

        public string SmtpUser { get; set; }

        public string SmtpPass { get; set; }

        public EmailService(string smtpHost, int smtpPort, string smtpUser, string smtpPass)
        {
            this.SmtpHost = smtpHost;
            this.SmtpPort = smtpPort;
            this.SmtpUser = smtpUser;
            this.SmtpPass = smtpPass;
        }

        public void SendEmail(MailMessage msg)
        {
            try
            {
                using (SmtpClient client = new SmtpClient()
                {
                    UseDefaultCredentials = false,
                    Credentials = new System.Net.NetworkCredential(SmtpUser, SmtpPass),
                    Port = SmtpPort,
                    Host = SmtpHost,
                    DeliveryMethod = SmtpDeliveryMethod.Network,
                    EnableSsl = true
                })
                {
                    client.Send(msg);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message + " | " + ex.InnerException);
            }
        }

        public MailMessage Get_Mailmessage(string to, string subject, string body)
        {
            MailMessage msg = new MailMessage();
            msg.To.Add(new MailAddress(to));
            msg.From = new MailAddress(SmtpUser);
            msg.Subject = subject;
            msg.Body = body;
            msg.IsBodyHtml = true;
            return msg;
        }

        public MailMessage Get_Mailmessage_With_iCalAttachment(string to, string mail_subject, string mail_Body, string iCal_body, string iCal_summary, string iCal_location, DateTime iCal_startDate)
        {
            MailMessage msg = Get_Mailmessage(to, mail_subject, mail_Body);
            string iCalAtt = Get_iCal(to, iCal_summary, iCal_body, iCal_startDate, iCal_location);
            System.Net.Mail.Attachment attachment = System.Net.Mail.Attachment.CreateAttachmentFromString(iCalAtt, new ContentType("text/calendar"));
            attachment.TransferEncoding = TransferEncoding.Base64;
            attachment.Name = "Mødeindkaldelse.ics";
            msg.Attachments.Add(attachment);

            return msg;
        }

        private string Get_iCal(string to, string summary, string body, DateTime startDate, string location)
        {
            iCalendar iCal = new iCalendar();
            iCal.Method = "PUBLISH";
            Event evt = iCal.Create<Event>();

            evt.Summary = summary;
            evt.Start = new iCalDateTime(startDate.Year, startDate.Month, startDate.Day, startDate.Hour, startDate.Minute, startDate.Second);
            evt.End = evt.Start.AddMinutes(15);
            evt.IsAllDay = false;
            evt.Description = body;
            evt.Location = location;

            iCalendarSerializer serializer = new iCalendarSerializer(iCal);
            return serializer.SerializeToString();
        }
    }
}