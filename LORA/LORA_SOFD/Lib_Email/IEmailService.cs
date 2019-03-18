using System;
using System.Net.Mail;

namespace Lib._365
{
    public interface IEmailService
    {
        string SmtpHost { get; set; }
        int SmtpPort { get; set; }
        string SmtpUser { get; set; }
        string SmtpPass { get; set; }
        void SendEmail(MailMessage msg);
        MailMessage Get_Mailmessage(string to, string subject, string body);
        MailMessage Get_Mailmessage_With_iCalAttachment(string to, string mail_subject, string mail_Body, string iCal_body, string iCal_summary, string iCal_location, DateTime iCal_startDate);
    }
}